from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://behavior_db_2niw_user:7VfygdESPlJEjidlwdD0bfHTuiMgIjiM@dpg-d60agpkr85hc739drv1g-a.virginia-postgres.render.com/behavior_db_2niw"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE behavior_history
        ADD COLUMN IF NOT EXISTS state TEXT;
    """))

print("✅ Column 'state' added successfully")