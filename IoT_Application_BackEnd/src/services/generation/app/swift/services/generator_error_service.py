def generate_error_service() -> str:
    """
    This function generates the error service.
    :return: The error service.
    """
    return f"""import Foundation
import Amplify
import AWSAPIPlugin
import ESPProvision

{__generate_generic_error()}
{__generate_auth_common_error()}
{__generate_cloud_error_message()}
{__generate_remote_common_error()}
{__generate_ESP_provision_common_error()}
{__generate_mqtt_error()}
{__generate_web_RTC_error()}
{__generate_error_service_class()}
"""


def __generate_generic_error() -> str:
    """
    This function generates the generic common error.
    :return: The generic common error.
    """
    return """protocol CommonError: Error {
    var code: Int { get }
}

enum GenericCommError: CommonError {
    
    case illegalState
    case decodeEncode
    case timeout
    
    public var code:Int {
        switch self {
        case .illegalState:
            return 1101
        case .decodeEncode:
            return 1102
        case .timeout:
            return 1103
        }
    }
}
"""


def __generate_auth_common_error() -> str:
    """
    This function generates the generic common error.
    :return: The generic common error.
    """
    return """
public enum AuthCommError: CommonError {
    
    case configuration
    case service(errorDescription: String, error: Error? = nil)
    case unknown
    case validation(field: String, errorDescription: String)
    case notAuthorized(errorDescription: String)
    case invalidState
    case signedOut
    case sessionExpired
    
    public var code: Int {
        switch self {
        case .configuration:
            return 2101
        case .service:
            return 2102
        case .unknown:
            return 2103
        case .validation:
            return 2104
        case .notAuthorized:
            return 2105
        case .invalidState:
            return 2106
        case .signedOut:
            return 2107
        case .sessionExpired:
            return 2108
        }
    }
}
    """


def __generate_cloud_error_message() -> str:
    """
    This function generates the cloud error message.
    :return: The struct of the cloud error message.
    """
    return """struct CloudErrorMessage: Codable {
    var code: Int
    var message: String
    
    enum CodingKeys: String, CodingKey {
        case code = "Code"
        case message = "Message"
    }
}
    """


def __generate_remote_common_error() -> str:
    """
    This function generates the remote common error.
    :return: The remote common error.
    """
    return """enum RemoteCommError: CommonError {
    
    case server(statusCode: Int, message: String?)
    case unknown
    case network
    case operation
    case invalidURL
    case invalidConfiguration
    case plugin
    
    public var code:Int {
        switch self {
        case .server(let statusCode, _):
            return 3000 + statusCode
        case .unknown:
            return 3601
        case .network:
            return 3602
        case .operation:
            return 3603
        case .invalidURL:
            return 3604
        case .invalidConfiguration:
            return 3605
        case .plugin:
            return 3606
        }
    }
    
    func getServerMessage() -> CloudErrorMessage? {
        var cloudErrorMessage: CloudErrorMessage? = nil
        switch self {
        case .server(_, let message):
            if let message = message?.data(using: .utf8) {
                do {
                    let decodedMessage = try JSONDecoder().decode(CloudErrorMessage.self, from: message)
                    cloudErrorMessage = decodedMessage
                }
                catch {
                    cloudErrorMessage = nil
                }
            }
        default:
            cloudErrorMessage = nil
        }
        return cloudErrorMessage
    }
}
    """


def __generate_ESP_provision_common_error() -> str:
    """
    This function generates the ESP Provision common error.
    :return: The ESP Provision common error.
    """
    return """enum ESPProvisionCommError: CommonError {
    
    case cameraNotAvailable
    case cameraAccessDenied
    case bluetoothNotAvailable
    case videoError
    case invalidQRCode
    case espDeviceNotFound
    case transportTypeNotAvailable
    
    case sessionInitError
    case sessionNotEstablished
    case sendDataError
    case securityMismatch
    case versionInfoError
    case bleFailedToConnect
    case encryptionError
    case decryptionError
    case noPOP
    case noUsername
    
    case communicationError
    case responseError
    case sessionError
    
    
    public var code:Int {
        switch self {
        case .cameraNotAvailable:
            return 4101
        case .cameraAccessDenied:
            return 4102
        case .bluetoothNotAvailable:
            return 4103
        case .videoError:
            return 4104
        case .invalidQRCode:
            return 4105
        case .espDeviceNotFound:
            return 4106
        case .transportTypeNotAvailable:
            return 4107
            
        case .sessionInitError:
            return 4201
        case .sessionNotEstablished:
            return 4202
        case .sendDataError:
            return 4203
        case .securityMismatch:
            return 4204
        case .versionInfoError:
            return 4205
        case .bleFailedToConnect:
            return 4206
        case .encryptionError:
            return 4207
        case .decryptionError:
            return 4208
        case .noPOP:
            return 4209
        case .noUsername:
            return 4210
            
        case .communicationError:
            return 4301
        case .responseError:
            return 4302
        case .sessionError:
            return 4303
        }
    }
}
    """


def __generate_mqtt_error() -> str:
    """
    This function generates the MQTT error.
    :return: The MQTT error.
    """
    return """enum MQTTError: CommonError {
    
    case publish
    case subscribe
    case unknown
    
    public var code:Int {
        switch self {
        case .publish:
            return 5101
        case .subscribe:
            return 5102
        case .unknown:
            return 5103
        }
    }
}
    """


def __generate_web_RTC_error() -> str:
    """
    This function generates the WebRTC error.
    :return: The WebRTC error.
    """
    return """
enum WebRTCError: CommonError {
    
    case session(statusCode: Int)
    case describeSignalingChannel
    case getSignalingChannelEndpoint
    case sign
    case getIceServerConfig
    case addPeerConnection
    case setPeerConnectionRemoteDescription
    case audioSession
    case kinesisVideoClientCreation
    case sendOffer
    
    public var code:Int {
        switch self {
        case .session(let statusCode):
            return 6000 + statusCode
        case .describeSignalingChannel:
            return 6101
        case .getSignalingChannelEndpoint:
            return 6102
        case .sign:
            return 6103
        case .getIceServerConfig:
            return 6104
        case .addPeerConnection:
            return 6105
        case .setPeerConnectionRemoteDescription:
            return 6106
        case .audioSession:
            return 6107
        case .kinesisVideoClientCreation:
            return 6108
        case .sendOffer:
            return 6109
        }
    }
}
    """


def __generate_error_service_class() -> str:
    """
    This function generates the error service class.
    :return: The error service class.
    """
    return """class ErrorsService {
    
    static func buildAPIErrorResult<T>(error: APIError) -> Result<T, Error> {
        switch error {
        case .httpStatusError(let statusCode, let response):
            if let urlResponse = response as? AWSHTTPURLResponse, let body = urlResponse.body {
                let str = String(decoding: body, as: UTF8.self)
                return .failure(RemoteCommError.server(statusCode: statusCode, message: str))
            } else {
                return .failure(RemoteCommError.server(statusCode: statusCode, message: nil))
            }
        case .unknown(_, _, _):
            return .failure(RemoteCommError.unknown)
        case .invalidConfiguration(_, _, _):
            return .failure(RemoteCommError.invalidConfiguration)
        case .invalidURL(_, _, _):
            return .failure(RemoteCommError.invalidURL)
        case .operationError(_, _, _):
            return .failure(RemoteCommError.operation)
        case .networkError(_, _, _):
            return .failure(RemoteCommError.network)
        case .pluginError(_):
            return .failure(RemoteCommError.plugin)
        }
    }
    
    static func buildAuthErrorResult<T>(error: AuthError) -> Result<T, Error> {
        switch error {
        case .configuration(_, _, _):
            return .failure(AuthCommError.configuration)
        case .service(let errorDescription, _, let error):
            return .failure(AuthCommError.service(errorDescription: errorDescription, error: error))
        case .unknown(_, _):
            return .failure(AuthCommError.unknown)
        case .validation(let field, let errorDescription, _, _):
            return .failure(AuthCommError.validation(field: field, errorDescription: errorDescription))
        case .notAuthorized(let errorDescription, _, _):
            return .failure(AuthCommError.notAuthorized(errorDescription: errorDescription))
        case .invalidState(_, _, _):
            return .failure(AuthCommError.invalidState)
        case .signedOut(_, _, _):
            return .failure(AuthCommError.signedOut)
        case .sessionExpired(_, _, _):
            return .failure(AuthCommError.sessionExpired)
        }
    }
}
    """
