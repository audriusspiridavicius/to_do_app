from rest_framework.response import Response

class StepResponse(Response):

    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        
        steps_count = len(data)if isinstance(data, list) else 1
        
        result = {
            "steps count":steps_count,
            "steps":data

            }
        
        data = result

        
        super().__init__(data, status, template_name, headers, exception, content_type)
