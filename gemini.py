def paraphrase_content(model, comment, language):        
    try:
        query = f""" Your task is to return just a paraphrase version of the following text in {language} language while maintaining its original meaning: {comment} """
        response = model.generate_content(query)
        
        return response.text
    except Exception as e:
        return None