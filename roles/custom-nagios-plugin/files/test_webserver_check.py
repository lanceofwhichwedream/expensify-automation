from webserver_check import check_hosts
from webserver_check import get_hosts
from webserver_check import sanitize_hosts
from webserver_check import combine_results

def test_check_hosts(mocker):
    """
    Function to test check_hosts
    """

    mock_data = 200

    mock_response = mocker.MagicMock()
    mock_response.status_code.return_value = mock_data
    mock_check_hosts = mocker
    mock_check_hosts.patch("requests.get", return_value=mock_response)

    result = check_hosts("http://192.168.1.1")

    print(result())
    print(mock_data)

    assert result() == mock_data
    assert type(result()) is int


def test_get_hosts(tmp_path):
    """
    Function to test get_hosts
    """
    temp_dir = tmp_path / "my_temp_dir"
    temp_dir.mkdir()

    temp_file = temp_dir / "webhosts.txt"
    temp_file.write_text("35.87.105.161\n35.95.108.99\n\n")

    hosts = get_hosts()
    print(hosts)

    assert hosts
    assert hosts == ["35.87.105.161", "35.95.108.99"]


def test_sanitize_hosts():
    """
    Function to test sanitize hosts
    """

    hosts = ["35.87.105.161", "35.95.108.99"]

    output = sanitize_hosts(hosts)

    assert output == ["http://35.87.105.161", "http://35.95.108.99"]
    assert output != hosts

def test_combine_results():
    """
    Function to test combine results
    """
    good_output = [200, 200]
    eh_output = [200, 404]
    bad_output = [404, 404]

    good_count = combine_results(good_output)
    eh_count = combine_results(eh_output)
    bad_count = combine_results(bad_output)

    assert good_count == 0
    assert eh_count == 1
    assert bad_count == 2