from rest_framework import serializers

class CustomListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):

        existing_records = {record.id:record for record in instance}

        created_records = []
        updated_records = []
        error_records = []
        for record in validated_data:
            
            record_id = record.get("id", None)
            record_error = record.get("has_error", None)
            if record_error:
                error_records.append(record)
            else:
                if record_id:
                    
                    existing_record = existing_records.get(record_id, None)
                    if existing_record:
                    
                        record_serializer = self.child.__class__(existing_record,record)
                        if record_serializer.is_valid():
                            updated_records.append(record_serializer.save())
                        # update existing task
                        else:
                            error_records.append(record_serializer.errors|existing_record.__dict__)
                    else:
                        #create new task
                        record_serializer = self.child.__class__(data=record)
                        if record_serializer.is_valid():
                                created_records.append(record_serializer.save())

        return {
            "created":created_records,
            "updated":updated_records,
            "errors": error_records
        }

    def to_internal_value(self, data):

        validated_data = []

        for record in data:
            record_serializer = self.child.__class__(data=record)
            if not record_serializer.is_valid():
                record["has_error"] = True
                record["error"] = record_serializer.errors
            validated_data.append(record)

        return validated_data
    
    def to_representation(self, data):
        return super().to_representation(data)