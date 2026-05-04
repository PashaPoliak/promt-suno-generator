import json
import os
import re

def parse_json(path):
    res = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.json'):
                with open(os.path.join(root, f), 'r', encoding='utf-8') as src:
                    try:
                        data = json.load(src)
                        items = data.get("data", []) if isinstance(data, dict) else data
                        if not isinstance(items, list): items = [data]
                        for item in items:
                            # Handle both direct text answers and index-based answers
                            ans = item.get("correctAnswer") or ""
                            if not ans:
                                opts = item.get("options", [])
                                keys = item.get("correct_answers", [])
                                if keys and opts:
                                    try:
                                        idx = ord(str(keys[0]).upper()) - 65
                                        if 0 <= idx < len(opts): ans = opts[idx]
                                    except: ans = keys[0]

                            # Handle explanations array
                            explanation = item.get("explanation") or ""
                            if not explanation and "explanations" in item:
                                explanations = item["explanations"]
                                correct_key = keys[0] if keys else ""
                                for exp in explanations:
                                    if exp.get("option") == correct_key:
                                        explanation = exp.get("explanation", "")
                                        break

                            question = item.get("question", "")
                            # Remove options from question text
                            question = re.sub(r'\n\*.*?(?=\n|\Z)', '', question, flags=re.DOTALL)
                            res.append({
                                "question": question,
                                "correctAnswer": ans,
                                "explanation": explanation
                            })
                    except: continue
    return res

def parse_ts(path):
    res = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.ts') or f.endswith('.js'):
                with open(os.path.join(root, f), 'r', encoding='utf-8') as src:
                    content = src.read()
                    blocks_iter = re.finditer(r'\{[\s\S]*?question:\s*"(.*?)"[\s\S]*?correctAnswer:\s*"(.*?)"[\s\S]*?explanation:\s*"(.*?)"[\s\S]*?\}', content)
                    for match in blocks_iter:
                        block_text = match.group(0)
                        q = match.group(1).strip()
                        a_letter = match.group(2).strip()
                        e = match.group(3).strip()
                        # Extract all option label/text pairs from within the same block
                        option_entries = re.findall(
                            r'\{\s*label:\s*"([A-D])",\s*text:\s*"(.*?)"\s*\}',
                            block_text,
                            re.DOTALL
                        )
                        correct_answer = a_letter
                        for label, text in option_entries:
                            if label == a_letter:
                                correct_answer = text.strip()
                                break
                        res.append({"question": q, "correctAnswer": correct_answer, "explanation": e})
    return res

def parse_md(path):
    res = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.md'):
                with open(os.path.join(root, f), 'r', encoding='utf-8') as src:
                    content = src.read()
                    content = re.sub(r' of \d+', '', content)
                    # Match each question block including its header
                    for match in re.finditer(r'^(### Question(?:\s+\d+)?\s*)$\n(.*?)(?=^### Question|\Z)', content, re.DOTALL | re.MULTILINE):
                        b = match.group(2)
                        # Format: details/summary
                        if "<details>" in b:
                            q = re.search(r'\*\*Scenario:\*\*.*?\n\n(.*?)(?=\n\*\*A\.\*\*|\n<details>|\n---)', b, re.DOTALL)
                            a = re.search(r'<summary>Correct Answer</summary>\n\n(.*?)\n\n', b, re.DOTALL)
                            e = re.search(r'</summary>\n\n(.*?)(?=\n</details>)', b, re.DOTALL)
                            question = q.group(1).strip() if q else ""
                            correct_answer = a.group(1).strip().strip('*') if a else ""
                            if question:
                                res.append({
                                    "question": question,
                                    "correctAnswer": correct_answer if correct_answer else (e.group(1).strip() if e else ""),
                                    "explanation": e.group(1).strip() if e else ""
                                })
                        # Format: Answer/Justification
                        else:
                            q = re.search(r'^(.*?)(?=\n\* |\n### Answer|\n---|$)', b, re.DOTALL)
                            a = re.search(r'### Answer\n\n(.*?)\n\n', b, re.DOTALL)
                            e = re.search(r'### Justification\n\n(.*?)(?=\n---|$)', b, re.DOTALL)
                            question = q.group(1).strip() if q else ""
                            correct_answer = a.group(1).strip().strip('*') if a else ""
                            if question:
                                res.append({
                                    "question": question,
                                    "correctAnswer": correct_answer if correct_answer else (e.group(1).strip() if e else ""),
                                    "explanation": e.group(1).strip() if e else ""
                                })
    return res

if __name__ == "__main__":
    base = "./exam-prep"
    j_data = parse_json(base)
    m_data = parse_md(base)
    t_data = parse_ts(base)

    all_items = j_data + m_data + t_data
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write("const examData = ")
        json.dump({"data": all_items}, f, indent=2)
        f.write(";")

    print(f"JSON: {len(j_data)} | MD: {len(m_data)} | TS/JS: {len(t_data)}")
    print(f"Total Exported: {len(all_items)}")