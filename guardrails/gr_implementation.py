from guardrails import Guard, OnFailAction
from guardrails.hub import RegexMatch
import re
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#nltk.download()
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

#pattern = re.compile(r'^(\+1|1)?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')

# Initialize the Guard with 
guard = Guard().use(RegexMatch(regex="^[A-Z][a-z]*$"))

try:
    print(guard.parse("Caesar").validation_passed)  # Guardrail Passes
    print(guard.parse("Caesar Salad").validation_passed)  
except Exception as e:
    print('Exception Occurred', e)


from guardrails import Guard, OnFailAction
from guardrails.hub import ToxicLanguage
from guardrails.hub import CompetitorCheck

guard = Guard().use_many(
    ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail=OnFailAction.EXCEPTION),
    CompetitorCheck(["Apple", "Microsoft", "Google"], on_fail=OnFailAction.EXCEPTION),
    
)

try:
    print('One')
    guard.validate(
        """An apple a day keeps a doctor away.
        This is good advice for keeping your health."""
    )  # Both the guardrails pass


    print('One')
    guard.validate(
        """Shut the hell up! Apple just released a new iPhone."""
    )  # Both the guardrails fail
except Exception as e:
    print(e)