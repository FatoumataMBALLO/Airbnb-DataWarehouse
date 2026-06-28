def check_dimension(df, key_column, name):
    print("\n" + "=" * 50)
    print(f"TEST {name}")
    print("=" * 50)

    print(df.head())

    print("\nNombre de lignes :", len(df))
    print("Nombre de colonnes :", len(df.columns))

    print("\nColonnes :")
    print(df.columns.tolist())

    print("\nValeurs nulles :")
    print(df.isna().sum())

    print(f"\nDoublons {key_column} :", df[key_column].duplicated().sum())