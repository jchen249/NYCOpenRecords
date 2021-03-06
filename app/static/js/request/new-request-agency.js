/**
 * Created by atan on 9/14/16.
 */

/* globals characterCounter: true */
/* globals getRequestAgencyInstructions: true */
/* globals getCustomRequestForms: true */
/* globals toggleRequestAgencyInstructions: true */
/* globals renderCustomRequestForm: true */
/* globals processCustomRequestForms: true */
/* globals requiredFields: true */

"use strict";

$(document).ready(function () {
    $(window).load(function () {
        // Determine if the agencyRequestInstructions and custom request forms need to be shown on page load.
        getRequestAgencyInstructions();
        getCustomRequestForms($("#request-agency").val());
    });

    $("input[name='tz-name']").val(jstz.determine().name());

    // Prevent user from entering a non numeric value into phone and fax field
    $("#phone").keypress(function (key) {
        if (key.charCode !== 0) {
            if (key.charCode < 48 || key.charCode > 57) {
                key.preventDefault();
            }
        }
    });
    $("#fax").keypress(function (key) {
        if (key.charCode !== 0) {
            if (key.charCode < 48 || key.charCode > 57) {
                key.preventDefault();
            }
        }
    });

    $("#request-agency").change(function () {
        getRequestAgencyInstructions();
        toggleRequestAgencyInstructions("hide");
        $(".appended-div").remove(); // remove the appended divs from previous agency
        previousValues = [];
        currentValues = [];
        getCustomRequestForms($("#request-agency").val());
    });

    $("#request-agency-instructions-toggle").click(function () {
        toggleRequestAgencyInstructions("default");
    });

    // render a new form every time a request type dropdown is changed
    $(document).on("focus", ".request-type", function () {
        var target = document.activeElement.id;
        target = target.replace("request-type-", "");
        var targetId = "#" + document.activeElement.id;
        $(targetId).off().change(function () {
            renderCustomRequestForm(target);
        });
    });

    // determine which dismiss button is being clicked
    $(document).on("click", ".panel-dismiss", function () {
        dismissTarget = "#" + document.activeElement.id;
    });

    // append a new dropdown and content div every time the additional content button is clicked
    $("#custom-request-form-additional-content").click(function () {
        customRequestFormCounter = customRequestFormCounter + 1;
        var dropdownTemplate = "<div class='panel panel-default appended-div' id='custom-request-panel-" + customRequestFormCounter + "'><div class='panel-heading' id='custom-request-forms-" + customRequestFormCounter + "' style='display: block;'><label class='request-heading request-type-label' for='request_type'>Request Type (optional)</label><button type='button' class='close panel-dismiss' id='panel-dismiss-button-" + customRequestFormCounter + "' data-target='#panel-dismiss-modal' data-toggle='modal'><span aria-hidden='true'>&times;</span><span class='sr-only'>Close</span></button><select class='input-block-level request-type' id='request-type-" + customRequestFormCounter + "' name='request_type'></select><br></div>";
        var contentTemplate = "<div class='panel-body' id='custom-request-form-content-" + customRequestFormCounter + "' hidden></div></div>";
        $(dropdownTemplate + contentTemplate).insertBefore("#custom-request-form-additional-content");
        $("#custom-request-form-additional-content").hide();

        // populate any empty dropdowns with that agency's form options
        populateDropdown($("#request-agency").val());

        previousValues[customRequestFormCounter - 1] = "";
        currentValues[customRequestFormCounter - 1] = "";
    });

    // javascript to add tooltip popovers when selecting the title and description
    $("#request-title").attr({
        'data-placement': "top",
        'data-trigger': "hover focus",
        'data-toggle': "popover",
        'data-content': "Public Advocate Emails from 2015",
        title: "Example Title"
    });
    $("#request-title").popover();
    // $("#request-title").click(function(){
    //     $("#request-title").popover("show");
    // });

    $("#request-description").attr({
        'data-placement': "top",
        'data-trigger': "hover focus",
        'data-toggle': "popover",
        'data-content': "Topic: Public Advocate Emails from 2015. Emails that mention bike lanes or bicycle lanes from the Public Advocate's Office between July 27, 2015 and September 10, 2015.",
        title: "Example Request"
    });
    $("#request-description").click(function () {
        $("#request-description").popover("show");
    });
    $("#request-description").popover();
    // $("#request-description").click(function(){
    //     $("#request-description").popover("show");
    // });

    // jQuery mask plugin to format fields
    $("#phone").mask("(999) 999-9999");
    $("#fax").mask("(999) 999-9999");
    $("#zipcode").mask("99999");

    // Datepicker for date request was received when creating a new request
    $(".dtpick").datepicker({
        dateFormat: "mm/dd/yy",
        maxDate: 0
    }).keydown(function (e) {
        // prevent keyboard input except for tab
        if (e.keyCode !== 9) {
            e.preventDefault();
        }
    });

    // Loop through required fields and apply a data-parsley-required attribute to them
    var requiredFields = ["request-title", "request-description", "first-name", "last-name", "email",
    "phone", "fax", "address-line-1", "method-received", "request-date", "city", "zipcode"];
    for (var i = 0; i < requiredFields.length; i++) {
        $("#" + requiredFields[i]).attr("data-parsley-required", "");
    }

    // Apply parsley validation styles to the input forms for a new request.
    $("#request-title").attr("data-parsley-maxlength", 90);
    $("#request-description").attr("data-parsley-maxlength", 5000);
    $("#first-name").attr("data-parsely-maxlength", 32);
    $("#last-name").attr("data-parsely-maxlength", 64);
    $("#email").attr("data-parsley-maxlength", 254);
    $("#user-title").attr("data-parsley-maxlength", 64);
    $("#user-organization").attr("data-parsley-maxlength", 128);
    $("#phone").attr("data-parsley-length", "[14,14]");
    $("#fax").attr("data-parsley-length", "[14,14]");
    $("#zipcode").attr("data-parsley-length", "[5,5]");

    // Custom Validation Messages
    $("#fax").attr("data-parsley-length-message", "The fax number must be 10 digits.");
    $("#phone").attr("data-parsley-length-message", "The phone number must be 10 digits.");
    $("#zipcode").attr("data-parsley-length-message", "The Zipcode must be 5 digits.");

    // Disable default error messages for email,phone,fax,address so custom one can be used instead.
    $("#phone").attr("data-parsley-required-message", "");
    $("#fax").attr("data-parsley-required-message", "");
    $("#address-line-1").attr("data-parsley-required-message", "");
    $("#city").attr("data-parsley-required-message", "");
    $("#email").attr("data-parsley-required-message", "");
    $("#zipcode").attr("data-parsley-required-message", "");

    // Limit the size of the file upload to 20 Mb. Second parameter is number of Mb's.
    $("#request-file").attr("data-parsley-max-file-size", "20");

    // Specify container for file input parsley error message
    $("#request-file").attr("data-parsley-errors-container", ".file-error");

    // Set name of the file to the text of filename div if file exists
    $("#request-file").change(function () {
        var file = this.files[0];
        var isChrome = window.chrome;

        if (file) {
            $("#filename").text((this.files[0].name));
        }
        // Cancel is clicked on upload window
        else {
            // If browser is chrome, reset filename text
            if (isChrome) {
                $("#filename").text("");
            }
        }
    });

    // Clear the file from input and the name from filename div
    $("#clear-file").click(function () {
        if ($(".file-error").is(":visible")) {
            $(".file-error").hide();
        }
        $("#request-file").val("");
        $("#filename").text("");
    });

    // Contact information validation
    $("#email").attr("data-parsley-type", "email");
    // Checks that at least one form of contact was filled out in addition to the rest of the form.
    $("#request-form").parsley().on("form:validate", function () {
        // Re-apply validators to fields in the event that they were removed from previous validation requests.
        for (var i = 0; i < requiredFields.length; i++) {
            $("#" + requiredFields[i]).attr("data-parsley-required", "");
        }
        // If address is filled out then make sure the city, state, and zipcode are filled.
        if ($("#address-line-1").parsley().isValid()) {
            $("#city").attr("data-parsley-required", "");
            $("#state").attr("data-parsley-required", "");
            $("#zipcode").attr("data-parsley-required", "");
        }
        // Checks that at least one of the contact information fields is filled in addition to the rest of the form
        if ($("#email").parsley().isValid() ||
            $("#phone").parsley().isValid() ||
            $("#fax").parsley().isValid() ||
            ($("#address-line-1").parsley().isValid() && $("#state").parsley().isValid() && $("#zipcode").parsley().isValid() && $("#city").parsley().isValid())
        ) {
            // If at least one of the fields are validated then remove required from the rest of the contact fields that aren't being filled out
            $("#city").removeAttr("data-parsley-required");
            $("#state").removeAttr("data-parsley-required");
            $("#zipcode").removeAttr("data-parsley-required");
            $("#phone").removeAttr("data-parsley-required");
            $("#fax").removeAttr("data-parsley-required");
            $("#address-line-1").removeAttr("data-parsley-required");
            $("#email").removeAttr("data-parsley-required");
        }
        else {
            // If none of the fields are valid then produce an error message and apply required fields.
            $(".contact-form-error-message").html("*At least one of the following must be filled out: Email, Phone, Fax, and/or Address (with City, State, and Zipcode)");
            $("#fax").attr("data-parsley-required", "");
            $("#phone").attr("data-parsley-required", "");
            $("#address-line-1").attr("data-parsley-required", "");
            $("#email").attr("data-parsley-required", "");
        }

        if ($("#request-file").parsley().isValid() === false) {
            $(".file-error").show();
        }
        else {
            $(".file-error").hide();
        }

        // Scroll to input label if parsley validation fails
        if ($("#request-title").parsley().isValid() === false) {
            $(window).scrollTop($(".title-label").offset().top);
        }
        else if ($("#request-description").parsley().isValid() === false) {
            $(window).scrollTop($(".description-label").offset().top);
        }
        else if ($("#request-file").parsley().isValid() === false) {
            $(".file-error").show();
            $(window).scrollTop($("#upload-control").offset().top);
        }
        else if ($("#method-received").parsley().isValid() === false) {
            $(window).scrollTop($(".format-label").offset().top);
        }
        else if ($("#first-name").parsley().isValid() === false) {
            $(window).scrollTop($(".first-name-label").offset().top);
        }
        else if ($("#last-name").parsley().isValid() === false) {
            $(window).scrollTop($(".last-name-label").offset().top);
        }
        else if ($("#email").parsley().isValid() === false) {
            $(window).scrollTop($(".email-label").offset().top);
        }
    });

    // Clear error messages for form.request_file on submit ...
    $("#submit").click(function () {
        $(".upload-error").remove();
    });
    // ... or on input change for request_file
    $("#request-file").change(function () {
        $(".upload-error").remove();
    });

    // Disable submit button on form submission
    $("#request-form").submit(function (e) {
        $(".remove-on-resubmit").remove();
        if ($("#request-form").parsley().isValid()) {
            var invalidForms = processCustomRequestFormData();
            if (invalidForms.length > 0) {
                e.preventDefault();
                $("#processing-submission").hide();
                $("#submit").show();
                $(window).scrollTop($(invalidForms[0]).offset().top);
                return;
            }
        }

        // Prevent multiple submissions
        $(this).submit(function () {
            return false;
        });
        $("#submit").hide();
        $("#processing-submission").show();
    });

    // Character count for creating a new request
    $("#request-title").keyup(function () {
        characterCounter("#title-character-count", 90, $(this).val().length);
    });

    $("#request-description").keyup(function () {
        characterCounter("#description-character-count", 5000, $(this).val().length);
    });

    $("#first-name").keyup(function () {
        characterCounter("#first-name-character-count", 32, $(this).val().length);
    });

    $("#last-name").keyup(function () {
        characterCounter("#last-name-character-count", 64, $(this).val().length);
    });

    $("#user-title").keyup(function () {
        characterCounter("#user-title-character-count", 64, $(this).val().length);
    });

    $("#user-organization").keyup(function () {
        characterCounter("#organization-character-count", 128, $(this).val().length);
    });

});
