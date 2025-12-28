import os
import time
import re
import logging
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SunoWebsiteParserSelenium:
    def __init__(self, base_url):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.visited_nav_items = set()  # Track visited navigation items
        self.output_dir = 'website_content_selenium'
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        self.actions = ActionChains(self.driver)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def sanitize_filename(self, text):
        """Convert text to a safe filename"""
        # Remove invalid characters
        safe = re.sub(r'[<>:"/\\|?*]', '_', text)
        # Replace multiple spaces with single underscore
        safe = re.sub(r'\s+', '_', safe)
        # Remove leading/trailing underscores
        safe = safe.strip('_')
        # Limit length
        return safe[:100] if safe else 'untitled'
    
    def create_folder_structure(self, category, subcategory=None):
        """Create folder structure based on navigation categories"""
        if subcategory:
            folder_path = os.path.join(self.output_dir, self.sanitize_filename(category), self.sanitize_filename(subcategory))
        else:
            folder_path = os.path.join(self.output_dir, self.sanitize_filename(category))
        
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    def save_current_content(self, category, subcategory=None, filename=None):
        """Save the current page's main content with proper categorization"""
        try:
            # Wait for main content to be present
            main_content = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            time.sleep(1)  # Additional wait for content to stabilize
            
            # Get the text content
            content_text = main_content.text
            
            # Create filename if not provided
            if not filename:
                current_url = self.driver.current_url
                url_path = urlparse(current_url).path.strip('/')
                if url_path:
                    filename = url_path.replace('/', '_')
                else:
                    filename = 'index'
                filename = self.sanitize_filename(filename)
            
            # Determine folder path
            if subcategory:
                folder_path = self.create_folder_structure(category, subcategory)
            else:
                folder_path = self.create_folder_structure(category)
            
            # Create file path
            file_path = os.path.join(folder_path, f"{filename}.txt")
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"URL: {self.driver.current_url}\n")
                f.write(f"Category: {category}\n")
                if subcategory:
                    f.write(f"Subcategory: {subcategory}\n")
                f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("\n" + "="*80 + "\n\n")
                f.write(content_text)
            
            logger.info(f"✓ Saved: {category}" + (f" > {subcategory}" if subcategory else "") + f" ({filename})")
            return True
            
        except Exception as e:
            logger.error(f"✗ Error saving content: {str(e)}")
            return False
    
    def expand_nav_item(self, nav_item):
        """Expand a collapsible navigation item if it has submenu"""
        try:
            # Check if this item has a dropdown/expandable submenu
            # Look for chevron or expand indicator
            try:
                chevron = nav_item.find_element(By.CSS_SELECTOR, "svg")
                
                # Check current state (expanded or collapsed)
                svg_classes = chevron.get_attribute('class') or ''
                
                # If it's not expanded (rotate-0 or similar), click to expand
                if 'rotate-0' in svg_classes or 'rotate-90' in svg_classes or 'rtl:rotate-180' not in svg_classes:
                    logger.debug(f"    ↳ Expanding submenu...")
                    chevron.click()
                    time.sleep(1)  # Wait for submenu to expand
                    return True
            except NoSuchElementException:
                # Try alternative selector for expandable elements
                try:
                    expand_button = nav_item.find_element(By.CSS_SELECTOR, "button, [role='button']")
                    # Check if this button has expand/collapse functionality by looking at its attributes
                    aria_expanded = expand_button.get_attribute('aria-expanded')
                    if aria_expanded == 'false':
                        logger.debug(f"    ↳ Expanding submenu via aria-expanded...")
                        expand_button.click()
                        time.sleep(1)
                        return True
                    elif aria_expanded is None:
                        # Check if the button contains an SVG that might be a chevron
                        chevrons = expand_button.find_elements(By.CSS_SELECTOR, "svg")
                        if chevrons:
                            # Click the button to expand
                            expand_button.click()
                            time.sleep(1)
                            return True
                except NoSuchElementException:
                    pass
                
        except (NoSuchElementException, StaleElementReferenceException):
            # No chevron found, so this item doesn't have a submenu
            pass
        except Exception as e:
            logger.warning(f"    ↳ Warning: Could not expand nav item: {str(e)}")
        
        return False
    
    def get_nav_items(self):
        """Get all navigation items from the sidebar"""
        nav_items = []
        
        try:
            # First try to find the main navigation container
            nav_selectors = [
                'div.nextra-scrollbar',
                'div[class*="nextra-menu"]',
                'nav',
                'div._overflow-y-auto._p-4._grow',
                'ul'
            ]
            
            for selector in nav_selectors:
                try:
                    nav_containers = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for nav_container in nav_containers:
                        # Find all list items in the navigation
                        container_items = nav_container.find_elements(By.CSS_SELECTOR, 'li')
                        if container_items:
                            nav_items.extend(container_items)
                            logger.info(f"Found {len(container_items)} navigation items using selector: {selector}")
                except NoSuchElementException:
                    continue
            
            # If still no nav items, try alternative approach
            if not nav_items:
                nav_items = self.driver.find_elements(By.CSS_SELECTOR, 'li._flex._flex-col._gap-1')
            
            # Remove duplicates while preserving order
            seen_items = set()
            unique_nav_items = []
            for item in nav_items:
                try:
                    item_id = item.get_attribute('id') or item.get_attribute('class') or item.text
                    if item_id not in seen_items:
                        seen_items.add(item_id)
                        unique_nav_items.append(item)
                except:
                    # If we can't get attributes, add the item anyway
                    unique_nav_items.append(item)
            
            nav_items = unique_nav_items
            
        except Exception as e:
            logger.error(f"Error finding navigation items: {str(e)}")
        
        return nav_items
    
    def process_nav_item(self, nav_item, depth=0, parent_category=None):
        """Process a single navigation item recursively"""
        try:
            # Get the link/text element inside the nav item
            try:
                link_element = nav_item.find_element(By.CSS_SELECTOR, 'a')
                link_text = link_element.text.strip()
            except NoSuchElementException:
                # Some items might be buttons instead of links
                try:
                    button_element = nav_item.find_element(By.CSS_SELECTOR, 'button')
                    link_element = button_element
                    link_text = button_element.text.strip()
                except NoSuchElementException:
                    # Skip items without clickable elements
                    return
            
            if not link_text or link_text in self.visited_nav_items:
                return
            
            print(f"{'  ' * depth}→ Processing: {link_text}")
            self.visited_nav_items.add(link_text)
            
            # Check if this item has submenu and expand it
            has_submenu = self.expand_nav_item(nav_item)
            
            # Click the main nav item
            try:
                link_element.click()
                time.sleep(2)  # Wait for content to load
                
                # Save the current content
                current_category = link_text
                # Check if this is a subcategory of a parent category
                is_main_category = link_text in [
                    "Suno prompt examples", "Complete guide", "Artist builder",
                    "Combination styles", "Common genres", "All music genres (6000+)",
                    "Lyric tags", "For Real Estate", "For Video Games", "Suno tutorials",
                    "Example prompts", "Making music", "Style and lyrics", "Common problems"
                ]
                
                if parent_category and not is_main_category:
                    # This is a subitem
                    self.save_current_content(parent_category, link_text)
                else:
                    # This is a top-level category
                    self.save_current_content(link_text)
                
                # If this item has a submenu, process subitems
                if has_submenu:
                    time.sleep(1)  # Wait for submenu to fully appear
                    
                    # Find subitems within this nav item
                    try:
                        # Look for nested list items - try multiple selectors
                        subitem_selectors = [
                            'ul li a',
                            'ul li button',
                            'div ul li a',
                            'div ul li button',
                            'li._flex._flex-col._gap-1 a',
                            'li._flex._flex-col._gap-1 button'
                        ]
                        
                        subitems = []
                        for selector in subitem_selectors:
                            try:
                                found_subitems = nav_item.find_elements(By.CSS_SELECTOR, selector)
                                if found_subitems:
                                    subitems = found_subitems
                                    break
                            except NoSuchElementException:
                                continue
                        
                        for subitem in subitems:
                            subitem_text = subitem.text.strip()
                            if subitem_text and subitem_text != link_text and subitem_text not in self.visited_nav_items:
                                print(f"{'  ' * (depth + 1)}↳ Subitem: {subitem_text}")
                                
                                # Save subitem content (click if needed)
                                try:
                                    # Store current URL to return to parent later
                                    parent_url = self.driver.current_url
                                    
                                    subitem.click()
                                    time.sleep(2)
                                    # Save as subcategory of the parent
                                    self.save_current_content(link_text, subitem_text)
                                    
                                    # Navigate back to parent page to continue processing
                                    self.driver.get(parent_url)
                                    time.sleep(1)
                                    
                                    # Re-expand the submenu after navigation
                                    if has_submenu:
                                        time.sleep(1)
                                        self.expand_nav_item(nav_item)
                                        
                                except Exception as e:
                                    print(f"{'  ' * (depth + 1)}✗ Error clicking subitem: {str(e)}")
                        
                    except Exception as e:
                        print(f"{'  ' * (depth + 1)}✗ Error finding subitems: {str(e)}")
                        pass
                
            except Exception as e:
                print(f"{'  ' * depth}✗ Error clicking {link_text}: {str(e)}")
            
        except Exception as e:
            print(f"{'  ' * depth}✗ Error processing nav item: {str(e)}")
    
    def parse_navigation(self):
        """Main method to parse the entire navigation structure"""
        print(f"Starting to parse navigation for: {self.base_url}")
        print("=" * 60)
        
        try:
            # Load the main page
            self.driver.get(self.base_url)
            time.sleep(3)  # Wait for initial load
            
            # Get all navigation items
            nav_items = self.get_nav_items()
            
            if not nav_items:
                print("✗ No navigation items found!")
                return
            
            # Process each navigation item
            for i, nav_item in enumerate(nav_items):
                try:
                    self.process_nav_item(nav_item)
                except StaleElementReferenceException:
                    # Element became stale, refresh the list
                    print(f"  ↻ Refreshing navigation list...")
                    nav_items = self.get_nav_items()
                    if i < len(nav_items):
                        self.process_nav_item(nav_items[i])
            
            print("=" * 60)
            print(f"\n✅ Parsing completed!")
            print(f"Total navigation items processed: {len(self.visited_nav_items)}")
            
            # Create summary file
            summary_path = os.path.join(self.output_dir, 'SUMMARY.txt')
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f"Website: {self.base_url}\n")
                f.write(f"Parsed on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total items processed: {len(self.visited_nav_items)}\n\n")
                
                f.write("NAVIGATION STRUCTURE:\n")
                f.write("=" * 50 + "\n")
                
                # Group by categories
                categories = {}
                for item in sorted(self.visited_nav_items):
                    # Determine if it's a main category or subcategory
                    if item in [
                        "Suno prompt examples", "Complete guide", "Artist builder", 
                        "Combination styles", "Common genres", "All music genres (6000+)",
                        "Lyric tags", "For Real Estate", "For Video Games", "Suno tutorials",
                        "Example prompts", "Making music", "Style and lyrics", "Common problems"
                    ]:
                        categories[item] = []
                        f.write(f"\n{item}\n")
                        f.write("-" * len(item) + "\n")
                    else:
                        # This is likely a subcategory
                        f.write(f"  • {item}\n")
                
        except Exception as e:
            print(f"✗ Fatal error during parsing: {str(e)}")
        
        finally:
            self.driver.quit()
            print(f"📁 Content saved in: {os.path.abspath(self.output_dir)}")

def main():
    website_url = "https://howtopromptsuno.com"
    parser = SunoWebsiteParserSelenium(website_url)
    parser.parse_navigation()

if __name__ == "__main__":
    main()