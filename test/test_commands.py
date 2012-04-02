import pytest

from command_execute import parse, execute
from command_execute import InvalidCommand, SingleCommandOnly, RunError, InStringError

class TestParse(object):
    def test_invalid_command(self):
        with pytest.raises(InvalidCommand):
            parse("su")
            parse("sed")
            parse("ls | less /etc/hosts")

    def test_single_command_only(self):
        with pytest.raises(SingleCommandOnly):
            parse("ls; less /etc/hosts")

    def test_unended_string(self):
        with pytest.raises(InStringError):
            parse("'ls | cat")
            parse('cat dog "dog')

    def test_invalid_char(self):
        parse("cat dog_bird Animals")
        parse('sed -e "s/.\\xanimal/dogbird#$%/g"')
        with pytest.raises(InvalidCommand):
            parse("cat dog.bird")
            parse("cat $cat")

    def test_parsing(self):
        commands = parse('cat dog | sed -e "s/DOG/CAT/g"')
        assert commands == [['cat', 'dog'], ['sed', '-e', '"s/DOG/CAT/g"']]

class TestExecute(object):
    def test_execeute_error(self):
        with pytest.raises(RunError):
            execute("cat nox")

    def test_valid_execute(self):
        execute("cat /home/divineslayer/dog")
        execute('sed "s/cat/bird/g" dog')
        execute('sed -e "s/cat/bird/g" dog')
        assert execute('cat dog | sed "s/cat/bird/g"').strip() == "birds and dogs until the end of time"
