"use strict";

describe("destroy: init plugin to test public method destroy", function() {

  beforeEach(function() {
    intlSetup();
    input = $("<input>");
    input.intlTelInput();
  });

  afterEach(function() {
    input = null;
  });

  it("adds the markup", function() {
    expect(getParentElement()).toHaveClass("intl-tel-input");
    expect(getSelectedFlagContainer()).toExist();
    expect(getListElement()).toExist();
  });


  describe("calling destroy", function() {

    beforeEach(function() {
      input.intlTelInput("destroy");
    });

    it("removes the markup", function() {
      expect(getParentElement()).not.toHaveClass("intl-tel-input");
      expect(getSelectedFlagContainer()).not.toExist();
      expect(getListElement()).not.toExist();
    });

  });

});




describe("destroy: init plugin with autoFormat enabled to test public method destroy", function() {

  beforeEach(function() {
    intlSetup();
    input = $("<input>");
    input.intlTelInput({
      autoFormat: true
    });
  });

  afterEach(function() {
    input = null;
  });

  it("binds the events listeners", function() {
    var listeners = $._data(input[0], 'events');
    expect("blur" in listeners).toBeTruthy();
    expect("focus" in listeners).toBeTruthy();
    // autoHideDialCode defaults to false now because nationalMode defaults to true
    //expect("mousedown" in listeners).toBeTruthy();
    expect("keyup" in listeners).toBeTruthy();
  });


  describe("calling destroy", function() {

    beforeEach(function() {
      input.intlTelInput("destroy");
    });

    it("unbinds the event listeners", function() {
      var listeners = $._data(input[0], 'events');
      expect(listeners).toBeUndefined();
    });

  });

});