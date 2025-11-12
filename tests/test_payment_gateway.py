from services.payment_service import PaymentGateway

def test_process_payment_success():
    gateway = PaymentGateway()
    success, txn_id, msg = gateway.process_payment("123456", 10.0, "Test payment")
    assert success
    assert "processed successfully" in msg

def test_process_payment_invalid_amount():
    gateway = PaymentGateway()
    success, txn_id, msg = gateway.process_payment("123456", 0, "Invalid payment")
    assert not success
    assert msg.startswith("Invalid amount")

def test_refund_payment_success():
    gateway = PaymentGateway()
    success, msg = gateway.refund_payment("txn_123456_1", 5.0)
    assert success
    assert "refund" in msg
