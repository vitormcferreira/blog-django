// import '../../vendor/jquery-3.6.3';

class InteractionManager {
  static interactionClass = 'interacted';

  constructor($btn) {
    this.$newInteraction = $btn.parents('.interaction');
    this.$interacteds = $btn.parents('.interactions').find('.interacted');
  }

  interact() {
    if (this.#alreadyInteractedWith()) {
      this.#undoInteract(this.$newInteraction);
      return;
    }

    if (this.#isUniqueInteraction()) {
      const $uniqueInteracted = this.$interacteds.filter('.unique-interaction');
      this.#undoInteract($uniqueInteracted);
    }

    this.#interact(this.$newInteraction);
  }

  #alreadyInteractedWith() {
    return this.$interacteds.is(this.$newInteraction);
  }

  #isUniqueInteraction() {
    return this.$newInteraction.hasClass('unique-interaction');
  }

  #interact($interaction) {
    this.#increaseCount($interaction);
    $interaction.addClass(InteractionManager.interactionClass);
  }

  #undoInteract($interaction) {
    this.#increaseCount($interaction, -1);
    $interaction.removeClass(InteractionManager.interactionClass);
  }

  #increaseCount($element, value = 1) {
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
