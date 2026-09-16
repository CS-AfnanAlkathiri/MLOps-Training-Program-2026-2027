import great_expectations as gx
import great_expectations.expectations as gxe


def validate_with_gx(data):
    """Validate incoming order data with Great Expectations."""
    context = gx.get_context(mode="ephemeral")

    data_source = context.data_sources.add_pandas(name="prediction_input_source")

    data_asset = data_source.add_dataframe_asset(name="prediction_input_asset")

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        name="prediction_input_batch"
    )

    suite = context.suites.add(gx.ExpectationSuite(name="prediction_input_suite"))

    suite.add_expectation(
        gxe.ExpectColumnValuesToNotBeNull(column="order_purchase_timestamp")
    )

    suite.add_expectation(
        gxe.ExpectColumnValuesToNotBeNull(column="order_estimated_delivery_date")
    )

    suite.add_expectation(
        gxe.ExpectColumnValuesToBeBetween(column="distance_km", min_value=0)
    )

    suite.add_expectation(
        gxe.ExpectColumnValuesToBeBetween(column="total_price", min_value=0)
    )

    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="customer_state"))

    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="seller_state"))

    suite.add_expectation(
        gxe.ExpectColumnValuesToBeInSet(
            column="customer_state",
            value_set=[
                "AC",
                "AL",
                "AP",
                "AM",
                "BA",
                "CE",
                "DF",
                "ES",
                "GO",
                "MA",
                "MT",
                "MS",
                "MG",
                "PA",
                "PB",
                "PR",
                "PE",
                "PI",
                "RJ",
                "RN",
                "RS",
                "RO",
                "RR",
                "SC",
                "SP",
                "SE",
                "TO",
            ],
        )
    )

    suite.add_expectation(
        gxe.ExpectColumnValuesToBeInSet(
            column="seller_state",
            value_set=[
                "AC",
                "AL",
                "AP",
                "AM",
                "BA",
                "CE",
                "DF",
                "ES",
                "GO",
                "MA",
                "MT",
                "MS",
                "MG",
                "PA",
                "PB",
                "PR",
                "PE",
                "PI",
                "RJ",
                "RN",
                "RS",
                "RO",
                "RR",
                "SC",
                "SP",
                "SE",
                "TO",
            ],
        )
    )

    suite.add_expectation(
        gxe.ExpectColumnValuesToBeOfType(column="total_price", type_="float")
    )

    suite.add_expectation(
        gxe.ExpectColumnValuesToBeOfType(column="distance_km", type_="float")
    )

    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="prediction_input_validation",
            data=batch_definition,
            suite=suite,
        )
    )

    result = validation_definition.run(batch_parameters={"dataframe": data})

    if not result.success:
        raise ValueError("Great Expectations validation failed.")

    return True
