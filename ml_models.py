import pandas as pd
from pandas.api.types import is_numeric_dtype

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


def prepare_data(df):
    data = df.copy()

    # Handle date columns
    for col in list(data.columns):

        if not is_numeric_dtype(data[col]):

            converted = pd.to_datetime(
                data[col],
                errors="coerce"
            )

            # Only treat the column as a date when
            # most values can be converted successfully.
            if converted.notna().mean() > 0.8:

                data[f"{col}_year"] = converted.dt.year
                data[f"{col}_month"] = converted.dt.month
                data[f"{col}_day"] = converted.dt.day
                data[f"{col}_dayofweek"] = converted.dt.dayofweek

                data.drop(
                    columns=[col],
                    inplace=True
                )

    # Encode remaining categorical/string columns
    for col in data.columns:

        if not is_numeric_dtype(data[col]):

            encoder = LabelEncoder()

            data[col] = encoder.fit_transform(
                data[col].astype(str)
            )

    # Convert everything to numeric
    data = data.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Handle missing values
    data = data.fillna(0)

    return data


def run_ml_model(df, target_column):

    # Determine target type BEFORE preprocessing.
    # Numeric target -> Regression
    # String/category/bool target -> Classification

    original_target = df[target_column]

    is_classification = not is_numeric_dtype(
        original_target
    )

    data = prepare_data(df)

    if target_column not in data.columns:

        raise ValueError(
            f"Target column '{target_column}' "
            f"could not be processed."
        )

    X = data.drop(
        columns=[target_column]
    )

    y = data[target_column]

    if len(X) < 5:

        raise ValueError(
            "Not enough data to train the model."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # -------------------------
    # CLASSIFICATION
    # -------------------------

    if is_classification:

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        preds = model.predict(
            X_test
        )

        score = accuracy_score(
            y_test,
            preds
        )

        return (
            "Classification",
            score
        )

    # -------------------------
    # REGRESSION
    # -------------------------

    else:

        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        preds = model.predict(
            X_test
        )

        score = r2_score(
            y_test,
            preds
        )

        return (
            "Regression",
            score
        )