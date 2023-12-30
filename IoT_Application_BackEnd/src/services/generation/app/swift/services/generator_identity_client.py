def generate_identity_client() -> str:
    """
    This function generates the identity client.
    :return: The identity client.
    """
    return f"""import Foundation
import Amplify
import AWSAPIPlugin


class IdentityClient {{
{__generate_methods()}
}}
    """


def __generate_methods() -> str:
    """
    This function generates the methods for the identity client.
    :return: The methods for the identity client.
    """
    return f"""
{__generate_logout()}
{__generate_get_auth_session()}
{__generate_confirm_signup()}
{__generate_resend_signup_code()}
{__generate_signIn()}
{__generate_confirm_signIn_with_new_password()}
{__generate_update_password()}
{__generate_reset_password()}
{__generate_confirm_reset_password()}
{__generate_signUp()}"""


def __generate_logout() -> str:
    """
    This function generates the logout method for the identity client.
    :return: The logout method for the identity client.
    """
    return """    func logout() async {
        let _ = await Amplify.Auth.signOut()
    }
    """


def __generate_get_auth_session() -> str:
    """
    This function generates the getAuthSession method for the identity client.
    :return: The getAuthSession method for the identity client.
    """
    return """    func getAuthSession() async -> Result<AuthSession, Error> {
        do {
            let result = try await Amplify.Auth.fetchAuthSession()
            return .success(result)
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """


def __generate_confirm_signup() -> str:
    """
    This function generates the confirmSignUp method for the identity client.
    :return: The confirmSignUp method for the identity client.
    """
    return """    func confirmSignUp(email: String, code: String) async -> Result<Void, Error> {
        do {
            let _ = try await Amplify.Auth.confirmSignUp(for: email, confirmationCode: code)
            return .successfulVoid
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """


def __generate_resend_signup_code() -> str:
    """
    This function generates the resendSignUpCode method for the identity client.
    :return: The resendSignUpCode method for the identity client.
    """
    return """    func resendSignUpCode(email: String) async -> Result<Void, Error> {
        do {
            let _ = try await Amplify.Auth.resendSignUpCode(for: email)
            return .successfulVoid
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """


def __generate_signIn() -> str:
    """
    This function generates the signIn method for the identity client.
    :return: The signIn method for the identity client.
    """
    return """    func signIn(username: String,  password: String) async -> Result<AuthSignInResult, Error> {
        do {
            let response = try await Amplify.Auth.signIn(username: username, password: password)
            return .success(response)
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch  {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """


def __generate_confirm_signIn_with_new_password() -> str:
    """
    This function generates the confirmSignInWithNewPassword method for the identity client.
    :return: The confirmSignInWithNewPassword method for the identity client.
    """
    return """    func confirmSignInWithNewPassword(password: String) async -> Result<AuthSignInResult, Error> {
        do {
            let response = try await Amplify.Auth.confirmSignIn(challengeResponse: password)
            return .success(response)
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch  {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """


def __generate_update_password() -> str:
    """
    This function generates the updatePassword method for the identity client.
    :return: The updatePassword method for the identity client.
    """
    return """    func updatePassword(old: String, new: String) async -> Result<Void, Error> {
        do {
            let _ = try await Amplify.Auth.update(oldPassword: old, to: new)
            return .successfulVoid
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch  {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """


def __generate_reset_password() -> str:
    """
    This function generates the resetPassword method for the identity client.
    :return: The resetPassword method for the identity client.
    """
    return """    func resetPassword(email: String) async -> Result<AuthResetPasswordResult, Error> {
        do {
            let result = try await Amplify.Auth.resetPassword(for: email)
            return .success(result)
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch  {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """


def __generate_confirm_reset_password() -> str:
    """
    This function generates the confirmResetPassword method for the identity client.
    :return: The confirmResetPassword method for the identity client.
    """
    return """    func confirmResetPassword(email: String, password: String, code: String) async -> Result<Void, Error> {
        do {
            let _ = try await Amplify.Auth.confirmResetPassword(for: email, with: password, confirmationCode: code)
            return .successfulVoid
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch  {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """


def __generate_signUp() -> str:
    """
    This function generates the signUp method for the identity client.
    :return: The signUp method for the identity client.
    """
    return """    func signUp(email: String, password: String) async -> Result<AuthSignUpResult, Error> {
        do {
            let result = try await Amplify.Auth.signUp(username: email, password: password)
            return .success(result)
        } catch let error as APIError {
            return ErrorsService.buildAPIErrorResult(error: error)
        } catch let error as AuthError {
            return ErrorsService.buildAuthErrorResult(error: error)
        } catch  {
            return .failure(GenericCommError.decodeEncode)
        }
    }
    """
