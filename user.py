from user_settings import user_settings

class User():
    
    def __init__(self, field_values: tuple[any]):
        self.id = str(field_values[0]) #dict_of_fields["userid"]
        self.state = int(field_values[1]) #dict_of_fields["state"]
        self.problem = str(field_values[2]) #dict_of_fields["problem"]
        self.answer = str(field_values[3]) #dict_of_fields["answer"]
        self.addition = bool(field_values[4]) #dict_of_fields["addition"]
        self.subtraction = bool(field_values[5]) #dict_of_fields["subtraction"]
        self.multiplication = bool(field_values[6]) #dict_of_fields["multiplication"]
        self.division = bool(field_values[7]) #dict_of_fields["division"]
        self.max_sum = int(field_values[8]) #dict_of_fields["max_sum"]
        self.max_factor = int(field_values[9]) #dict_of_fields["max_factor"]
        self.correct = int(field_values[10]) #dict_of_fields["correct"]
        self.incorrect = int(field_values[11]) #dict_of_fields["incorrect"]
        self.skipped = int(field_values[12]) #dict_of_fields["skipped"]
    
    def extract_settings(self) -> user_settings:
        settings = user_settings(self.addition, self.subtraction, 
                                 self.multiplication, self.division, 
                                 self.max_sum, self.max_factor)
        return settings