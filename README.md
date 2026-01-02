# Suno Prompt Generator
[![Python application](https://github.com/PashaPoliak/promt-suno-generator/actions/workflows/python-app.yml/badge.svg)](https://github.com/PashaPoliak/promt-suno-generator/actions/workflows/python-app.yml)

##[API]
v1 - sqlite
v2 - json
v3 - pg

cd ./app && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
taskkill /f /im python.exe
taskkill /f /im node.exe
py -m pytest tests/ -v
./test_api.sh

DONT USE COMMENTS AND LOGGER
your changes break v1
run 
cd ./app && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

check ./test_api.sh

fix errors
v1 -sqlite, v3 -pg
must be work both db



## Project Overview
This project is a Suno prompt generator with both frontend and backend components, designed to help users create better prompts for the Suno AI music platform.

https://studio-api.prod.suno.com/api/profiles/fghjkl11?playlists_sort_by=upvote_count&clips_sort_by=created_at&include_hooks=true
https://studio-api.prod.suno.com/api/clip/d057f1e9-ba96-41e9-a0d9-c21370ed7f9b
https://studio-api.prod.suno.com/api/clip/3084c7bb-5260-4f94-b799-6faaa53528d0
https://studio-api.prod.suno.com/api/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at
https://studio-api.prod.suno.com/api/profiles/fotballpiraten
https://studio-api.prod.suno.com/api/playlist/7ec624f7-9a8d-4a9c-84a6-33132901e1cc
https://studio-api.prod.suno.com/api/clip/c49e393c-b98e-4c2d-a03a-36c05841a9d1

http://localhost:8000/api/v2/playlist
http://localhost:8000/api/v2/playlist/574c5144-2eb5-44e1-9333-3add06c84006
http://localhost:8000/api/v2/playlist/7ec624f7-9a8d-4a9c-84a6-33132901e1cc

http://localhost:8000/api/v2/clip
http://localhost:8000/api/v2/clip/d057f1e9-ba96-41e9-a0d9-c21370ed7f9b
http://localhost:8000/api/v2/clip/3084c7bb-5260-4f94-b799-6faaa53528d0
http://localhost:8000/api/v2/clip/c49e393c-b98e-4c2d-a03a-36c05841a9d1

http://localhost:8000/api/v2/profiles
http://localhost:8000/api/v2/profiles/fotballpiraten
http://localhost:8000/api/v2/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at


http://localhost:8000/api/v1/playlist
http://localhost:8000/api/v1/playlist/574c5144-2eb5-44e1-9333-3add06c84006
http://localhost:8000/api/v1/playlist/7ec624f7-9a8d-4a9c-84a6-33132901e1cc

http://localhost:8000/api/v1/clip
http://localhost:8000/api/v1/clip/d057f1e9-ba96-41e9-a0d9-c21370ed7f9b
http://localhost:8000/api/v1/clip/3084c7bb-5260-4f94-b799-6faaa53528d0
http://localhost:8000/api/v1/clip/c49e393c-b98e-4c2d-a03a-36c05841a9d1

http://localhost:8000/api/v1/profiles
http://localhost:8000/api/v1/profiles/fotballpiraten
http://localhost:8000/api/v1/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at

curl -s "http://localhost:8000/api/v1/playlist" | python -m json.tool


##[React]

`npm start dev`

```bash
npx create-react-app ui --template typescript
npm install @types/node@^20.19.0 --save-dev
npm install -D vite @vitejs/plugin-react tailwindcss postcss autoprefixer
npm install tailwindcss-animate eslint @eslint/eslintrc
npm install -D tailwindcss
npm install react-router-dom @mui/material @emotion/react @emotion/styled
npm install react-plotly.js plotly.js-basic-dist-min
npm install --save-dev @types/plotly.js
npm install --save-dev @types/react-router-dom
npm install react-router-dom@latest
npm install axios
npm install --save-dev @types/axios
npm install -D tailwindcss postcss autoprefixer
npm install -D tailwindcss@3
npx tailwindcss init -p
```
cd frontend && npm install
`npm start dev`

`npm test -- --coverage --watchAll=false --reporters=jest-html-reporter > ui-test-results.md`

`npm run build`

`npm install @modelcontextprotocol/sdk`

`npm i -D @modelcontextprotocol/inspector`
