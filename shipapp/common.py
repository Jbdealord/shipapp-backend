#Author: Debojit Kaushik ( 11th April 2017 )

from rest_framework.response import Response
from rest_framework import status


#Error Class.
class error_codes(object):
		#ERROR CODES
		_SERVER_ERROR	=	status.HTTP_500_INTERNAL_SERVER_ERROR
		_BAD_PARAM		=	status.HTTP_400_BAD_REQUEST 
		_NOT_FOUND		=	status.HTTP_404_NOT_FOUND
		_FORIDDEN		=	status.HTTP_403_FORBIDDEN
		_OK				=	status.HTTP_200_OK
		_UNAUTHORISED	=	status.HTTP_401_UNAUTHORIZED

		#ERROR MESSAGES.
		_ASSERTION_ERROR	=	"Please Check Parameters."
		_EXCEPTION_ERROR	=	"We encountered a problem. Please report this."
		_NOT_FOUND_ERROR	=	"Entity could not be found."
		_UNAUTHORISED_ERROR	=	"User not allowed to perform this function."

#Common response handler.
def api_response( success , status , data = None , error = None ):
	if success is True and data is not None:
		return Response({
			'success'	:	True,
			'data'		:	data,
			},status)
	elif success is False and error is not None:
		return Response({
			'success'	:	False,
			'error'		:	error,
			}, status)
	else:
		return Response({
			'success'	:	False,
			'message'	:	"We encountered an internal Problem. Please report this to our admin team."
			}, status)