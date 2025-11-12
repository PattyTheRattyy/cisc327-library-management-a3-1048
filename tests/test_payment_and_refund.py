import pytest
from unittest.mock import Mock
from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway





# pay late fees testing
def test_pay_late_fees_success(mocker):
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 5.0, "days_overdue": 3, "status": "late fee"}
    )
    mocker.patch(
        "services.library_servicGe.get_book_by_id",
        return_value={"id": 1, "title": "1984", "author": "George Orwell"}
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123456", "Payment successful")

    success, message, txn_id = pay_late_fees("123456", 1, mock_gateway)
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=5.0,
        description="Late fees for '1984'"
    )

    assert success is True
    assert "successful" in message.lower()
    assert txn_id == "txn_123456"


def test_pay_late_fees_payment_declined(mocker):
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 1500.0, "days_overdue": 10, "status": "late fee"}
    )
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id": 2, "title": "A testing book"}
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Payment declined")

    success, message, txn_id = pay_late_fees("123456", 2, mock_gateway)
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=1500.0,
        description="Late fees for 'A testing book'"
    )

    assert success is False
    assert "failed" in message.lower()
    assert txn_id is None


def test_pay_late_fees_invalid_patron_id(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book")
    mocker.patch("services.library_service.get_book_by_id")

    mock_gateway = Mock(spec=PaymentGateway)

    success, message, txn_id = pay_late_fees("12", 1, mock_gateway)
    mock_gateway.process_payment.assert_not_called()
    assert success is False
    assert "invalid patron id" in message.lower()
    assert txn_id is None


def test_pay_late_fees_zero_fee(mocker):
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 0.0, "days_overdue": 0, "status": "no fee"}
    )
    mock_gateway = Mock(spec=PaymentGateway)

    success, message, txn_id = pay_late_fees("123456", 1, mock_gateway)
    mock_gateway.process_payment.assert_not_called()
    assert success is False
    assert "no late fees" in message.lower()
    assert txn_id is None


def test_pay_late_fees_network_error(mocker):
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 5.0, "days_overdue": 2, "status": "late fee"}
    )
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id": 3, "title": "How to win at chess"}
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("Network error")

    success, message, txn_id = pay_late_fees("123456", 3, mock_gateway)
    mock_gateway.process_payment.assert_called_once()
    assert success is False
    assert "error" in message.lower()
    assert txn_id is None








# refund tests
def test_refund_late_fee_success(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund successful")

    success, message = refund_late_fee_payment("txn_123456", 5.0, mock_gateway)

    mock_gateway.refund_payment.assert_called_once_with("txn_123456", 5.0)
    assert success is True
    assert "successful" in message.lower()


def test_refund_late_fee_invalid_transaction_id(mocker):
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("", 5.0, mock_gateway)
    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert "invalid transaction id" in message.lower()


def test_refund_late_fee_invalid_amounts(mocker):
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("txn_123456", -5.0, mock_gateway)
    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert "greater than 0" in message.lower()

    success, message = refund_late_fee_payment("txn_123456", 0.0, mock_gateway)
    assert success is False
    assert "greater than 0" in message.lower()

    success, message = refund_late_fee_payment("txn_123456", 20.0, mock_gateway)
    assert success is False
    assert "exceeds maximum" in message.lower()
