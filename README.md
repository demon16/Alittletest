# init
```bash
pip3 install -r requirements.txt
sudo apt install python3-alembic
python3-alembic init alembic
python3 model.py
python3 view.py
```
# database upmigrate or update
```bash
python3-alembic revision --autogenerate -m "your comment about this migrate or update"
python3-alembic upgrade head
```