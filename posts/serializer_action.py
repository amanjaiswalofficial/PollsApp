from rest_framework import status
from .error_messages import *
from .database_queries import DBQueries


def get_question_set_call(args_dict):
    current_queryset = args_dict.get('current_queryset')
    response = DBQueries().get_data_from_querset(current_queryset)
    response_status_code = status.HTTP_200_OK
    return response, response_status_code

def get_question_call(args_dict):
    response, response_code = DBQueries().get_objects_from_queryset(**args_dict)
    if response:
        return set_response_and_code(response, status.HTTP_200_OK)
    else:
        return NO_QUESTION_FOUND_ERROR, response_code


def create_question_call(args_dict):
    serializer = args_dict.get('serializer')
    current_user = args_dict.get('current_user')
    if not current_user.is_anonymous:
        if serializer.is_valid():
            try:
                DBQueries().perform_create_question(serializer, current_user)
                response = serializer.data
                response_status_code = status.HTTP_201_CREATED
            except:
                response = INTERNAL_SERVER_ERROR
                response_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response = serializer.errors
            response_status_code = status.HTTP_400_BAD_REQUEST
    else:
        response = INVALID_CREDENTIAL_ERROR
        response_status_code = status.HTTP_400_BAD_REQUEST
    return response, response_status_code


def update_question_call(args_dict):
    current_user = args_dict.pop('current_user')
    permission = args_dict.pop('permissions')[0]
    request_data = args_dict.pop('request_data')
    response, response_status = DBQueries().get_object_from_queryset(**args_dict)
    if response:
        if not permission.has_object_permission(current_user, response):
            return AUTHORIZATION_ERROR, status.HTTP_401_UNAUTHORIZED
        args_dict.update({'data': request_data})
        DBQueries().update_question(**args_dict)
        return CHOICE_UPDATE_SUCCESSFUL_MESSAGE, status.HTTP_200_OK
    else:
        return NO_QUESTION_FOUND_ERROR, response_status


def delete_question_call(args_dict):
    current_user = args_dict.pop('current_user')
    permission = args_dict.pop('permissions')[0]
    response, response_status = DBQueries().get_object_from_queryset(**args_dict)
    if response:
        if not permission.has_object_permission(current_user, response):
            return AUTHORIZATION_ERROR, status.HTTP_401_UNAUTHORIZED
        DBQueries().delete_object_from_queryset(**args_dict)
        return CHOICE_DELETE_SUCCESSFUL_MESSAGE, status.HTTP_200_OK
    else:
        return NO_QUESTION_FOUND_ERROR, status.HTTP_400_BAD_REQUEST


def create_choice_call(args_dict):
    current_user = args_dict.pop('current_user')
    choice_model, question_model = args_dict.get('current_model')[0], args_dict.get('current_model')[1]
    permission = args_dict.pop('permissions')[0]
    serializer = args_dict.pop('serializer')
    request_data = args_dict.get('request_data')
    if serializer.is_valid():
        question_pk = request_data.get('question')
        response, response_status = DBQueries().get_object_from_queryset(current_queryset=question_model, pk=question_pk)
        if response:
            if not permission.has_object_permission(current_user, response):
                return set_response_and_code(AUTHORIZATION_ERROR, status.HTTP_401_UNAUTHORIZED)
            DBQueries().perform_create_choice(serializer)
            return set_response_and_code(serializer.data, status.HTTP_201_CREATED)
        else:
            return set_response_and_code(NO_QUESTION_FOUND_ERROR, status.HTTP_400_BAD_REQUEST)
    else:
        return set_response_and_code(serializer.errors, status.HTTP_400_BAD_REQUEST)


def update_choice_call(args_dict):
    filter_values ={}
    current_user = args_dict.pop('current_user')
    choice_model = args_dict.pop('current_model')
    question_model = args_dict.pop('other_model')
    permission = args_dict.pop('permissions')[0]
    request_data = args_dict.get('request_data')
    question_pk = request_data.get('question')
    choice_pk = request_data.get('id')
    question_response, response_status = DBQueries().get_object_from_queryset(current_queryset=question_model,
                                                                     pk=question_pk)
    if question_response:
        if not permission.has_object_permission(current_user, question_response):
            return set_response_and_code(AUTHORIZATION_ERROR, status.HTTP_400_BAD_REQUEST)
        choice_response, response_status = DBQueries().get_object_from_queryset(current_queryset=choice_model,
                                                                         pk=choice_pk)
        if not choice_response:
            return set_response_and_code(NO_CHOICE_FOUND_ERROR, status.HTTP_400_BAD_REQUEST)
        for item, value in request_data.items():
            filter_values[item] = value
        filter_values['question'] = question_response
        DBQueries().update_choice(current_object=choice_response, filter_value=filter_values)
        return set_response_and_code(CHOICE_UPDATE_SUCCESSFUL_MESSAGE, status.HTTP_200_OK)
    else:
        return set_response_and_code(NO_QUESTION_FOUND_ERROR, status.HTTP_400_BAD_REQUEST)


def delete_choice_call(args_dict):
    current_user = args_dict.pop('current_user')
    choice_model = args_dict.pop('current_model')
    question_model = args_dict.pop('other_model')
    permission = args_dict.pop('permissions')[0]
    request_data = args_dict.get('request_data')
    question_pk = request_data.get('question')
    choice_pk = request_data.get('id')
    question_response, response_status = DBQueries().get_object_from_queryset(current_queryset=question_model,
                                                                              pk=question_pk)
    if question_response:
        if not permission.has_object_permission(current_user, question_response):
            return set_response_and_code(AUTHORIZATION_ERROR, status.HTTP_400_BAD_REQUEST)
        choice_response, response_status = DBQueries().get_object_from_queryset(current_queryset=choice_model,
                                                                                pk=choice_pk)
        if not choice_response:
            return set_response_and_code(NO_CHOICE_FOUND_ERROR, status.HTTP_400_BAD_REQUEST)
        DBQueries().delete_query(current_object=choice_response)
        return set_response_and_code(CHOICE_DELETE_SUCCESSFUL_MESSAGE, status.HTTP_200_OK)
    else:
        return set_response_and_code(NO_QUESTION_FOUND_ERROR, status.HTTP_400_BAD_REQUEST)

def get_choice_set_call(args_dict):
    choice_model = args_dict.pop('current_model')
    question_model = args_dict.pop('other_model')
    question_pk = args_dict.pop('pk')
    question_response, response_code = DBQueries().get_object_from_queryset(current_queryset=question_model,
                                                              pk=question_pk)
    if question_response:
        choices_response, response_code = DBQueries().get_objects_from_queryset(current_queryset=choice_model,
                                                                 question=question_response)
        return set_response_and_code(choices_response, status.HTTP_200_OK)
    else:
        return set_response_and_code(NO_QUESTION_FOUND_ERROR, status.HTTP_400_BAD_REQUEST)

def perform_action(**kwargs):
    args_dict = {}
    for parameter, value in kwargs.items():
        args_dict[parameter] = value
    api_call = get_api_name(args_dict.pop('action_type'))
    return api_call(args_dict)


def get_api_name(input_str):
    api_call_dictionary = {'create_question': create_question_call,
                           'get_question_set': get_question_set_call,
                           'get_question': get_question_call,
                           'update_question': update_question_call,
                           'delete_question': delete_question_call,
                           'create_choice': create_choice_call,
                           'get_choice_set': get_choice_set_call,
                           'update_choice': update_choice_call,
                           'delete_choice': delete_choice_call,
                           'get_choice_set':get_choice_set_call}
    return api_call_dictionary[input_str]


def set_response_and_code(response, response_code):
    response = response
    response_code = response_code
    return response, response_code