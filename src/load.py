from pathlib import Path
import pandas as pd


def save_tables(
    dim_property,
    dim_host,
    dim_location,
    dim_date,
    fact_availability,
    fact_reviews,
):
    """Sauvegarde toutes les dimensions et tables de faits dans le Warehouse."""

    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "Warehouse"

    try:
        # Création sécurisée du dossier
        output_dir.mkdir(parents=True, exist_ok=True)

        # Cartographie des DataFrames et de leurs chemins cibles
        tables_to_save = {
            "dim_property": (dim_property, output_dir / "dim_property.csv"),
            "dim_host": (dim_host, output_dir / "dim_host.csv"),
            "dim_location": (dim_location, output_dir / "dim_location.csv"),
            "dim_date": (dim_date, output_dir / "dim_date.csv"),
            "fact_availability": (fact_availability, output_dir / "fact_availability.csv"),
            "fact_reviews": (fact_reviews, output_dir / "fact_reviews.csv"),
        }

        # Sauvegarde dynamique avec retour utilisateur
        print("💾 Début de la sauvegarde dans le Warehouse...")
        for name, (df, path) in tables_to_save.items():
            if df is None or df.empty:
                print(f"⚠️ Le DataFrame '{name}' est vide ou absent. Sauvegarde ignorée.")
                continue

            df.to_csv(path, index=False)
            print(f"  -> {name}.csv sauvegardé ({len(df)} lignes)")

            # Si les fichiers CSV restent trop lourds / trop lents à relire,
            # décommente les 2 lignes suivantes pour sauvegarder aussi en
            # Parquet (5-10x plus compact, bien plus rapide à relire) :
            # df.to_parquet(path.with_suffix(".parquet"), index=False)
            # print(f"  -> {name}.parquet sauvegardé également")

        # Vérification globale (Optionnel mais rassurant)
        print("\n🔍 Vérification du Warehouse :")
        property_path = tables_to_save["dim_property"][1]

        if property_path.exists():
            test = pd.read_csv(property_path, nrows=3)
            print(f"✅ Exemple réussi avec dim_property. Colonnes : {test.columns.tolist()}")

        print("\n🎉 Toutes les tables valides ont été sauvegardées avec succès !")

    except PermissionError:
        print(f"❌ Erreur de droits : Impossible d'écrire dans le dossier {output_dir}. Vérifiez qu'un fichier n'est pas ouvert ailleurs (ex: Excel).")
    except Exception as e:
        print(f"❌ Une erreur critique est survenue lors de la sauvegarde : {str(e)}")