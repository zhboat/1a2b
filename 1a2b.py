import random
import click
import signal

GAME_RULE = (
    'Suppose the answer is "9527", user must try to guess the true answer.\n'
    '"A" means the digit is at right position.'
    '"B" means the digit is at wrong position.\n'
    '* "1234" -> 0A1B\n'
    '* "5678" -> 0A2B\n'
    '* "9726" -> 2A1B\n'
    '* "9627" -> 3A0B\n'
    '* "9527" -> 4A0B'
)

GAME_PROMPT = (
    "The system generates a four-digit random number "
    "with different bit orders.\n"
    "Please enter your guess and follow the prompts "
    "to get the correct answer of the random number."
)

TIMEOUT = 240


def generate_correct_digit() -> str:
    digit = map(str, random.sample(range(10), 4))
    return "".join(digit)


def check_user_guess_digit(user_guess_digit: str, correct_digit: str) -> bool:
    if user_guess_digit == correct_digit:
        click.echo("Congratulations! The %s is right!" % correct_digit)
        return True
    elif len(user_guess_digit) != 4:
        raise ValueError("Length error!")
    elif len(user_guess_digit) > len(set(user_guess_digit)):
        raise ValueError("Input repeatable!")
    elif not all(i.isdigit() for i in user_guess_digit):
        raise ValueError("Input error!")
    else:
        _check_user_guess_digit(user_guess_digit, correct_digit)


def _check_user_guess_digit(user_guess_digit: str, correct_digit: str) -> None:
    a, b = 0, 0
    for i, j in zip(user_guess_digit, correct_digit):
        if i == j:
            a += 1
        elif i in correct_digit:
            b += 1

    click.echo("%sa%sb" % (a, b))


def input_digit(prompt: str) -> str:
    def timeout_handler(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIMEOUT)
    try:
        user_guess_digit = click.prompt(prompt)
        signal.alarm(0)
        return user_guess_digit
    except TimeoutError:
        click.echo("\nTime is out, please try again later.")
        raise


@click.command()
@click.option("--rule", is_flag=True, help="Display game rules.")
def run(rule: str) -> None:
    if rule:
        click.echo(GAME_RULE)
        return

    prompt = "\nPlease input your guess four-digit: "
    correct_digit = generate_correct_digit()
    while True:
        try:
            check_user_guess_digit(input_digit(prompt), correct_digit)
            prompt = "\nYour guess is not correct, please try again: "
        except (ValueError, TimeoutError) as e:
            click.echo(str(e))
            break
        except Exception:
            raise


if __name__ == "__main__":
    click.echo(GAME_PROMPT)
    run()
