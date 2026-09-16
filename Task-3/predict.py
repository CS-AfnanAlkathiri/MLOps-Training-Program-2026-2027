import argparse

from src.data_access import load_csv_data
from src.prediction import predict_order


def main():
    parser = argparse.ArgumentParser(
        description="Predict whether Olist orders will be delivered late."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to a CSV file containing order data."
    )

    args = parser.parse_args()

    data = load_csv_data(args.input)
    predictions = predict_order(data)

    for result in predictions:
        print(result)


if __name__ == "__main__":
    main()