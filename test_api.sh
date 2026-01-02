#!/bin/bash

ENDPOINTS=(    
    # V1 User endpoints
    "http://localhost:8000/api/v1/users"

    # V1 Playlist endpoints
    "http://localhost:8000/api/v1/playlists/574c5144-2eb5-44e1-9333-3add06c84006"
    "http://localhost:8000/api/v1/playlists/7ec624f7-9a8d-4a9c-84a6-33132901e1cc"
    "http://localhost:8000/api/v1/playlists"
    
    # V1 Clip endpoints
    "http://localhost:8000/api/v1/clips/d057f1e9-ba96-41e9-a0d9-c21370ed7f9b"
    "http://localhost:8000/api/v1/clips/3084c7bb-5260-4f94-b799-6faaa53528d0"
    "http://localhost:8000/api/v1/clips/c49e393c-b98e-4c2d-a03a-36c05841a9d1"
    "http://localhost:8000/api/v1/clips"
    
    # V1 Profile endpoints
    "http://localhost:8000/api/v1/profiles/fotballpiraten"
    "http://localhost:8000/api/v1/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at"
    "http://localhost:8000/api/v1/profiles"

    # V2 Playlist endpoints
    "http://localhost:8000/api/v2/playlists"
    "http://localhost:8000/api/v2/playlists/574c5144-2eb5-44e1-933-3add06c84006"
    "http://localhost:8000/api/v2/playlists/7ec624f7-9a8d-4a9c-84a6-33132901e1cc"
    
    # V2 Clip endpoints
    "http://localhost:8000/api/v2/clips"
    "http://localhost:8000/api/v2/clips/d057f1e9-ba96-41e9-a0d9-c21370ed7f9b"
    "http://localhost:8000/api/v2/clips/3084c7bb-5260-4f94-b799-6faaa53528d0"
    "http://localhost:8000/api/v2/clips/c49e393c-b98e-4c2d-a03a-36c05841a9d1"
    
    # V2 Profile endpoints
    "http://localhost:8000/api/v2/profiles"
    "http://localhost:8000/api/v2/profiles/fotballpiraten"
    "http://localhost:8000/api/v2/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at"


    # V3 Playlist endpoints
    "http://localhost:8000/api/v3/playlists"
    "http://localhost:8000/api/v3/playlists/574c5144-2eb5-44e1-9333-3add06c84006"
    "http://localhost:8000/api/v3/playlists/7ec624f7-9a8d-4a9c-84a6-33132901e1cc"
    
    # V3 Clip endpoints
    "http://localhost:8000/api/v3/clips"
    "http://localhost:8000/api/v3/clips/d057f1e9-ba96-41e9-a0d9-c21370ed7f9b"
    "http://localhost:8000/api/v3/clips/3084c7bb-5260-4f94-b799-6faaa53528d0"
    "http://localhost:8000/api/v3/clips/c49e393c-b98e-4c2d-a03a-36c05841a9d1"
    
    # V3 Profile endpoints
    "http://localhost:8000/api/v3/profiles"
    "http://localhost:8000/api/v3/profiles/fotballpiraten"
    "http://localhost:8000/api/v3/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at"
)

total_tests=0
passed_tests=0
failed_tests=0

echo "Starting API endpoint tests..."

for endpoint in "${ENDPOINTS[@]}"; do
    ((total_tests++))
    echo -n "curl $endpoint ... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$endpoint")
    
    if [ "$response" = "200" ]; then
        json_response=$(curl -s "$endpoint")
        if echo "$json_response" | python -m json.tool > /dev/null 2>&1; then
            echo "PASS (Status: $response, Valid JSON)"
            ((passed_tests++))
        else
            echo "FAIL (Status: $response, Invalid JSON)"
            ((failed_tests++))
        fi
    else
        ((failed_tests++))
    fi
done

echo "================================"
echo "Test Summary:"
echo "Total tests: $total_tests"
echo "Passed: $passed_tests"
echo "Failed: $failed_tests"

if [ $failed_tests -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi