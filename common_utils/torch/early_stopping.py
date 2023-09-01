# Inspired by https://debuggercafe.com/using-learning-rate-scheduler-and-early-stopping-with-pytorch/

class EarlyStopping:
    """
    Detects whether the loss has stopped decreasing so that training can be halted early.
    """
    patience: int
    steps_since_last_improvement: int = 0
    lowest_loss: float = float("inf")

    def __init__(self, patience: int):
        """
        :param patience: Training will be stopped if the loss hasn't decreased for this many steps
        """
        self.patience = patience

    def __call__(self, loss) -> bool:
        """
        This should be called after each epoch to detect whether training should stop.
        :param loss: This epoch's (validation) loss
        :return: True, if training should stop
        """
        if loss < self.lowest_loss:
            # loss improved => reset timer
            self.steps_since_last_improvement = 0
            self.lowest_loss = loss
            return False
        else:
            self.steps_since_last_improvement += 1
            return self.steps_since_last_improvement >= self.patience
