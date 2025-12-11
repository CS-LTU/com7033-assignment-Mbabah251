def validate_assessment_data(hypertension, ever_married, work_type, residence_type, 
                            avg_glucose_level, bmi, smoking_status, stroke):
    """Validate assessment form data"""
    
    # Check required fields
    if not all([hypertension, ever_married, work_type, residence_type, 
                avg_glucose_level, bmi, smoking_status, stroke]):
        raise ValueError("All fields are required.")
    
    # Validate hypertension and stroke (0 or 1)
    if hypertension not in ['0', '1'] or stroke not in ['0', '1']:
        raise ValueError("Invalid hypertension or stroke value.")
    
    # Validate ever_married
    if ever_married not in ['No', 'Yes']:
        raise ValueError("Invalid marital status.")
    
    # Validate work_type
    valid_work_types = ['Children', 'Govt_job', 'Never_worked', 'Private', 'Self-employed']
    if work_type not in valid_work_types:
        raise ValueError("Invalid work type.")
    
    # Validate residence_type
    if residence_type not in ['Rural', 'Urban']:
        raise ValueError("Invalid residence type.")
    
    # Validate smoking_status
    valid_smoking = ['formerly smoked', 'never smoked', 'smokes', 'Unknown']
    if smoking_status not in valid_smoking:
        raise ValueError("Invalid smoking status.")
    
    # Validate numeric values
    try:
        glucose = float(avg_glucose_level)
        bmi_val = float(bmi)
        
        if glucose < 0 or glucose > 500:
            raise ValueError("Average glucose level must be between 0 and 500.")
        
        if bmi_val < 10 or bmi_val > 100:
            raise ValueError("BMI must be between 10 and 100.")
    except (ValueError, TypeError):
        raise ValueError("Invalid glucose level or BMI value.")