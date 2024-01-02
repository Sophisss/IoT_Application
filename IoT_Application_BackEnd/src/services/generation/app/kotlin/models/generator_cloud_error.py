def generate_cloud_error_model() -> str:
    """
    This method generates the CloudError model.
    :return: The CloudError model.
    """
    return """package models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class CloudError(
    @SerialName("Code") val code: Int? = null,
    @SerialName("Message") val message: String? = null
)
    """