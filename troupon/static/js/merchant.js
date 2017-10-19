$(document).ready(function () {

    // $('#datetimepicker').datetimepicker({
    //     timepicker:false,
    //     format:'Y-m-d',
    //     minDate: '0'
    // });

    function uploadbutton() {
        $('.btn-file :file').change(function (event) {
            label = $(this).val().split('\\');
            $(this).closest('span').after('<p>' + label[label.length - 1] + ' </p>')
        });
    }

    uploadbutton();

    var TokenGenerator = {
        goResend: function (event) {
            var _this = this;
            url = $(this).data('href');
            location.href = url
        },
        enableVerify: function (event) {
            if (this.$tokenField.val().length === 6) {
                this.$verifyButton.removeAttr('disabled');
            } else {
                this.$verifyButton.attr('disabled', 'disabled');
            }
        },
        $tokenField: $('#id_token_name'),
        $verifyButton: $('#id_verify_button'),
        $resendButton: $('#id_resend_button'),
        init: function () {
            this.$verifyButton.attr('disabled', 'disabled');
            this.applyEvents();
        },
        applyEvents: function () {
            this.$resendButton.on('click', this.goResend);
            this.$tokenField.on('keyup', this.enableVerify.bind(this));
        }
    }

    TokenGenerator.init();


    var DealEditingAbl = {
        $editDealBtn: $('#id_edit_deal_btn'),
        $cancelDealEditBtn: $('#id_cancel_deal_edit_btn'),
        $editDealEditForm: $('#id_deal_edit_form'),
        $dealDetailView: $('#id_deal_detail'),
        $dealQuorumCbx: $('#id_has_quorum_cbx'),
        $dealQuorumTbx: $('#id_quorum_tbx'),
        showEditForm: function (event) {
            event.preventDefault();
            this.$cancelDealEditBtn.toggleClass('hide');
            this.$editDealBtn.toggleClass('hide');
            this.$dealDetailView.toggleClass('hide');
            this.$editDealEditForm.toggleClass('hide');
        },
        showDealDetail: function (event) {
            event.preventDefault();
            this.$cancelDealEditBtn.toggleClass('hide');
            this.$editDealBtn.toggleClass('hide');
            this.$editDealEditForm.toggleClass('hide');
            this.$dealDetailView.toggleClass('hide');
        },
        toggleQuorumtbx: function (event) {
            this.$dealQuorumTbx.toggleClass('hide');
        },
        applyBinds: function () {
            this.$editDealBtn.on('click', this.showEditForm.bind(this));
            this.$cancelDealEditBtn.on('click', this.showDealDetail.bind(this));
            this.$dealQuorumCbx.on('click', this.toggleQuorumtbx.bind(this));
        },
        init: function () {
            this.applyBinds();
        }

    }

    DealEditingAbl.init();
});

$('#user-country').on('change', function (event) {
    var country = $(this).val();

    if (country == 0) {
        $('#nigerian-locations').addClass('hidden');
        $('#kenyan-locations').addClass('hidden');
    } else if (country == 1) {
        $('#nigerian-locations').removeClass('hidden');
        $('#kenyan-locations').addClass('hidden');
    } else if (country == 2) {
        $('#kenyan-locations').removeClass('hidden');
        $('#nigerian-locations').addClass('hidden');
    }
});

function previewImage() {
    var reader = new FileReader();
    reader.readAsDataURL(document.getElementById("file-upload").files[0]);
    reader.onload = function (event) {
        document.getElementById("merchant-logo").src = event.target.result;
    };
};