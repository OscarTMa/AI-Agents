import pandas as pd
from groq import Groq
import io

def execute_pandas_code(df, query, api_key):
    """
    1. Sends the Dataframe schema + User query to Groq.
    2. Receives Python code (Pandas).
    3. Executes the code and returns the result.
    """
    client = Groq(api_key=api_key)

    # 1. Prepare Context (Schema)
    columns = list(df.columns)
    sample_data = df.head(2).to_string()
    
    system_prompt = f"""
    You are a Python expert specializing in Data Analysis with Pandas.
    You are given a pandas DataFrame named `df`.
    
    Columns: {columns}
    Sample Data:
    {sample_data}
    
    Your task: Write a snippet of Python code to answer the user's question.
    
    RULES:
    1. Assume the dataframe `df` is already loaded.
    2. The code must store the final result in a variable named `result`.
    3. If the user asks for a plot, create a matplotlib figure and save it to `fig`.
    4. RETURN ONLY THE CODE. No markdown, no comments, no ```python``` tags. Just the code.
    """

    # 2. Get Code from LLM
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192", # 70b is smarter for coding
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0, # Deterministic for code
            stop=None
        )
        
        generated_code = completion.choices[0].message.content
        
        # Clean up code (sometimes LLMs still add markdown)
        generated_code = generated_code.replace("```python", "").replace("```", "").strip()

    except Exception as e:
        return f"Error connecting to Groq: {e}", None

    # 3. Execute Code safely
    # We create a local dictionary to store variables created by the exec()
    local_vars = {"df": df, "pd": pd}
    
    try:
        exec(generated_code, {}, local_vars)
        
        # Capture text result
        result = local_vars.get("result", "No result variable found in code.")
        
        # Capture plot if it exists (optional enhancement)
        # For simplicity, we stick to text/tables first, but you can inspect local_vars for 'plt'
        
        return result, generated_code

    except Exception as e:
        return f"Error executing code: {e}\nGenerated Code was:\n{generated_code}", generated_code
