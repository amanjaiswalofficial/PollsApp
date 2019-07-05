from rest_framework import status

from posts.error_messages import NO_QUESTION_FOUND_ERROR


class DBQueries():

    def perform_create_question(self, *args):
        serializer, current_user = args[0], args[1]
        serializer.save(created_by=current_user)

    def get_data_from_querset(self, *args):
        response = args[0].objects.all()
        return response

    def get_objects_from_queryset(self, **kwargs):
        current_queryset = kwargs.pop('current_queryset')
        response = current_queryset.objects.filter(**kwargs)
        if response:
            response_status_code = status.HTTP_200_OK
        else:
            response_status_code = status.HTTP_400_BAD_REQUEST
        return response, response_status_code

    def get_object_from_queryset(self, **kwargs):
        current_queryset = kwargs.pop('current_queryset')
        try:
            response = current_queryset.objects.get(**kwargs)
            return response, status.HTTP_200_OK
        except current_queryset.DoesNotExist:
            return False, status.HTTP_400_BAD_REQUEST

    def update_question(self, **kwargs):
        update_values = {}
        current_queryset = kwargs.pop('current_queryset')
        pk = kwargs.get('pk')
        data = kwargs.get('data')
        for keys, items in data.items():
            update_values[keys] = items
        response, status_code = self.get_object_from_queryset(current_queryset=current_queryset, pk=pk)
        self.update_query(response, **update_values)



    def delete_object_from_queryset(self, **kwargs):
        current_queryset = kwargs.get('current_queryset')
        pk = kwargs.get('pk')
        current_object = self.get_object_from_queryset(current_queryset=current_queryset, pk=pk)[0]
        current_object.delete()

    def perform_create_choice(self, *args):
        serializer = args[0]
        serializer.save()

    def update_choice(self, **kwargs):
        current_object = kwargs.pop('current_object')
        request_data = kwargs.get('filter_value')
        self.update_query(current_object, **request_data)

    def delete_query(self, **kwargs):
        current_object = kwargs.pop('current_object')
        current_object.delete()

    def update_query(self, object, **kwargs):
        for key, items in kwargs.items():
            setattr(object, key, items)
        object.save()