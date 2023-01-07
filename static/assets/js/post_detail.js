// import '../../vendor/jquery-3.6.3';

class InteractionManager {
  constructor($btn) {
    this.$newInteraction = $btn.parents('.unique-interaction');
    this.$oldInteraction = $btn
      .parents('.interactions')
      .find('.unique-interaction')
      .filter('.interacted');
  }

  interact() {
    const nothingSelected = this.$oldInteraction.length === 0;

    if (nothingSelected) {
      this._increaseCount(this.$newInteraction);
      this.$newInteraction.addClass('interacted');
      return;
    }
    // se o selecionado for o atual
    if (this.$oldInteraction.is(this.$newInteraction)) {
      this._increaseCount(this.$newInteraction, -1);
      this.$newInteraction.removeClass('interacted');
      return;
    }
    // se tiver um selecionado

    this._increaseCount(this.$oldInteraction, -1);
    this._increaseCount(this.$newInteraction);
    this.$oldInteraction.removeClass('interacted');
    this.$newInteraction.addClass('interacted');
  }

  _increaseCount($element, value = 1) {
    const $count = $element.find('.count-interactions');
    $count.text(Number($count.text()) + value);
  }
}

$('.btn-interact').on('click', function () {
  const $btn = $(this);

  $.post($btn.data('url'), {
    csrfmiddlewaretoken: $btn.data('csrf'),
  }).done(function () {
    const manager = new InteractionManager($btn);
    manager.interact();
  });
});
