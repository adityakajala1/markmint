import os
import sys
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models.core import Base

def migrate(source_url: str, target_url: str):
    # Handle postgres:// dialect on Render/Heroku natively
    if target_url.startswith("postgres://"):
        target_url = target_url.replace("postgres://", "postgresql://", 1)
        
    print(f"Source: {source_url}")
    print(f"Target: {target_url}")
    
    source_engine = create_engine(source_url)
    target_engine = create_engine(target_url)
    
    # Verify target tables exist
    target_meta = MetaData()
    target_meta.reflect(bind=target_engine)
    if not target_meta.tables:
        print("ERROR: Target database has no tables. Run `alembic upgrade head` first.")
        sys.exit(1)
        
    SourceSession = sessionmaker(bind=source_engine)
    TargetSession = sessionmaker(bind=target_engine)
    
    source_session = SourceSession()
    target_session = TargetSession()
    
    try:
        if target_engine.dialect.name == 'postgresql':
            try:
                target_session.execute(text("SET session_replication_role = 'replica';"))
            except Exception as e:
                print("Warning: Could not set session_replication_role (this is normal on managed DBs like Render). Continuing...")
                # The exception causes the transaction to abort in Postgres, so we must rollback before continuing
                target_session.rollback()
            
        for table in Base.metadata.sorted_tables:
            table_name = table.name
            print(f"Migrating table: {table_name}...")
            
            # Read all rows from source
            rows = source_session.execute(table.select()).all()
            if not rows:
                print(f"  - 0 rows")
                continue
                
            # Convert rows to dicts using _mapping
            row_dicts = [dict(row._mapping) for row in rows]
            
            # Insert into target
            target_session.execute(table.insert(), row_dicts)
            print(f"  - {len(rows)} rows migrated")
            
        target_session.commit()
        print("\nMigration completed successfully!")
        
    except Exception as e:
        target_session.rollback()
        print(f"\nMigration failed: {e}")
        sys.exit(1)
    finally:
        if target_engine.dialect.name == 'postgresql':
            try:
                target_session.execute(text("SET session_replication_role = 'origin';"))
                target_session.commit()
            except:
                pass
        source_session.close()
        target_session.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python migrate_sqlite_to_pg.py <SOURCE_URL> <TARGET_URL>")
        print("Example: python migrate_sqlite_to_pg.py sqlite:///./production_corpus.db postgresql+psycopg2://user:pass@localhost/db")
        sys.exit(1)
        
    source = sys.argv[1]
    target = sys.argv[2]
    migrate(source, target)
