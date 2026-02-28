from scripts.database import engine, Base
from scripts import models  # IMPORTANTE: carga los modelos

Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente")