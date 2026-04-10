## Use python3 -m api.testing.prompt_testing after cd into backend to successfully run the test cases. 
## Scroll to the bottom to see test cases.

## Note: Current prompt context and format is supplemented by confirmed general knowledge, will be removed after retrieval is working fully
from api.testing.test_cases import CASES
from api.services.rag_service import generate_answer


def evaluate_intent(actual_intent: str, expected_intent: str) -> bool: # compare actual intent with expected intent
    return actual_intent == expected_intent


def evaluate_answer_keywords(actual_answer: str, expected_keywords: list[str]):
    missing = []

    for keyword in expected_keywords: # loop through all keywords from the list of expected keywords and compare it to the actual answer
        if keyword.lower() not in actual_answer.lower():
            missing.append(keyword)

    if (len(expected_keywords) - len(missing))/len(expected_keywords) >= 0.80: # 80% accuracy was the determined threshold with Cleint for accuracy in terms of keywords
        return True, missing 

    return False, missing # return False if accuracy is below 0.8 and return a list of all missing keywords
 
## Doing below directly during pipeline now
#def build_context_from_docs(question: str, intent: str) -> str:
#    docs = retrieve_relevant_documents(question, INTENT_CONFIG[intent]["retrieval_k"]) # acquire the retrieved context for the prompt builder
#    return "\n\n".join([doc.page_content for doc in docs]) # acquire the context in text form for use in the prompt/response


def run_tests():
    results = [] # acquire a list of all the results

    for case in CASES: # loop through all test cases
        # acquire the needed details 
        question = case["question"]
        expected_intent = case["expected_intent"]
        expected_keywords = case["expected_keywords"]

        response = generate_answer(question) # generate response and run full pipeline. Returns intent, response, prompt, and sources
        actual_answer = response["answer"] # answer received

        # test for intent and matching keywords to test response accuracy based on test_file information
        intent_check = evaluate_intent(response["intent"], expected_intent) # Returns True if intent is matching, false if not
        answer_check, missing_keywords = evaluate_answer_keywords( # Returns True and an empty list if there are no missing keywords. For False, returns the missing keywords
            actual_answer,
            expected_keywords
        )

        results.append({ # list of information for the result of each test
            "id": case["id"], 
            "question": question,
            "actual_intent": response["intent"], # intent from testing intent_classification
            "intent_correct": intent_check,
            "answer_correct": answer_check, # based on missing keywords
            "missing_keywords": missing_keywords, # list of all missing keywords
            "built_prompt": response["prompt"], # the actual prompt
            "answer": actual_answer, # generated response
        })

    return results # return all the results to be displayed


if __name__ == "__main__": # Test Results should be displayed, hence main method should be used
    results = run_tests() # run all tests and receive a dict of information

    passed = 0 # Counter for all passed tests
    total = len(results) # total amount of results/test cases

    for result in results:
        print("-" * 80) # a line of --------...
        print("-" * 80) # a line of --------...
        print(f"TEST #{result['id']}") # Test Number
        print(f"Question: {result['question']}") # Question tested
        print(f"Actual Intent: {result['actual_intent']}") # Intent Found 
        print(f"Correct Intent Found: {result['intent_correct']}") # Intent Check
        print(f">= 80% Accurate Answer Check: {result['answer_correct']}") # 80% Accuracy Response Check
        print(f"Missing Keywords: {result['missing_keywords']}")
        print("\nBUILT PROMPT:\n")
        print(result["built_prompt"]) # Display the prompt used
        print("\nMODEL ANSWER:\n")
        print(result["answer"]) # display the received response
        print("-" * 80) # a line of --------...
        print("-" * 80) # a line of --------...

        if result["intent_correct"] and result["answer_correct"]: # For all checks passed
            passed += 1 # add 1 passed test to the tally


    print(f"\nPassed {passed}/{total} tests.") # Give the total number of passed tests out of the total