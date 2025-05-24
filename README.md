# COMP702 Prototypes
## Study Plan Algorithm
### Backend
1. Download Flask and z3-solver to your local computer on command terminal: 
```
pip install Flask
pip install z3-solver
```
2. Run file on command terminal:
```
python -m newtest run
```
If successful, it would show with this output (or similar):
```
 * Serving Flask app 'newtest'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: [000-000-000]
```
3. Open the link from the output in your browser, adding "/data" in the URL. For example: `http://127.0.0.1:5000/data`.
> As of May 2025, current file is `newtest.py`.
### Frontend
> As of May 2025, the current program is not fully implemented with new backend code. This only works with `test.py` which produces inaccurate results.
1. Run file on command terminal:
```
npm start
```
