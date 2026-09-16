import pandas as pd

from src.features import build_features


def preprocess_for_model(data, artifacts):
    """Apply the saved Task 2 preprocessing objects to new order data."""
    df = build_features(data)

    imputer = artifacts["imputer"]
    encoder = artifacts["encoder"]
    scaler = artifacts["scaler"]
    feature_list = artifacts["feature_list"]

    numeric_features = list(imputer.feature_names_in_)
    categorical_features = list(encoder.feature_names_in_)

    # Use the fitted imputer from Task 2.
    numeric_imputed = imputer.transform(df[numeric_features])

    numeric_df = pd.DataFrame(numeric_imputed, columns=numeric_features, index=df.index)

    # Use the fitted scaler from Task 2.
    numeric_scaled = scaler.transform(numeric_df)

    numeric_scaled_df = pd.DataFrame(
        numeric_scaled, columns=numeric_features, index=df.index
    )

    # Use the fitted one-hot encoder from Task 2.
    categorical_encoded = encoder.transform(df[categorical_features])

    encoded_feature_names = encoder.get_feature_names_out(categorical_features)

    categorical_df = pd.DataFrame(
        categorical_encoded, columns=encoded_feature_names, index=df.index
    )

    # Combine numerical and categorical features.
    final_features = pd.concat([numeric_scaled_df, categorical_df], axis=1)

    # Match the exact feature order used during training.
    final_features = final_features.reindex(columns=feature_list, fill_value=0)

    return final_features
