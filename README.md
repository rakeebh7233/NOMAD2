run env: env\Scripts\Activate
run backend: uvicorn main:app --reload
run frontend: npm start