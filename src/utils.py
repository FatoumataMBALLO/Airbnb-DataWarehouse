def check_dimension(df, key_column, label, foreign_keys=None):
    """
    Contrôle qualité générique pour une dimension ou une table de faits :
    - la clé technique existe
    - elle est unique
    - elle ne contient pas de valeurs nulles
    - (optionnel) les clés étrangères listées ne contiennent pas de nulls
      (ex: date_key, property_key dans une table de faits — un merge qui
      échoue silencieusement laisse ces colonnes à NaN sans jamais casser
      l'unicité de la clé technique elle-même).
    """
    if df is None:
        print(f"⚠️  {label} : DataFrame absent (None), contrôle ignoré.")
        return

    if key_column not in df.columns:
        print(f"❌ {label} : colonne clé '{key_column}' introuvable.")
        return

    if df.empty:
        print(f"⚠️  {label} : table vide, contrôle ignoré.")
        return

    n_total = len(df)
    n_unique = df[key_column].nunique()
    n_nulls = df[key_column].isna().sum()

    if n_unique != n_total:
        print(
            f"❌ {label} : {n_total - n_unique} doublons détectés "
            f"sur '{key_column}'."
        )
    elif n_nulls > 0:
        print(f"❌ {label} : {n_nulls} valeurs nulles sur '{key_column}'.")
    else:
        print(f"✅ {label} : {n_total} lignes, clé '{key_column}' valide.")

    if foreign_keys:
        for fk in foreign_keys:
            if fk not in df.columns:
                print(f"❌ {label} : clé étrangère '{fk}' introuvable.")
                continue
            fk_nulls = df[fk].isna().sum()
            if fk_nulls > 0:
                pct = fk_nulls / n_total * 100
                print(
                    f"❌ {label} : {fk_nulls} valeurs nulles sur la clé "
                    f"étrangère '{fk}' ({pct:.1f}% des lignes) — "
                    f"vérifier la jointure correspondante."
                )
            else:
                print(f"✅ {label} : clé étrangère '{fk}' sans valeur nulle.")