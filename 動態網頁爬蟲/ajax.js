var jqXHR = {
    "get_facility_map_data": null,
    "get_facility_popup_data": null,
    "get_facility_detail_data": null,
    "get_facility_data_list": null
};

// キャンセルリクエスト
function cancelRequest(name) {
    if (jqXHR[name]) {
        jqXHR[name].abort();
        jqXHR[name] = null;
    }
}

// 施設データリストを取得
function get_facility_map_data(condition) {
    // キャンセルリクエスト
    cancelRequest("get_facility_map_data");

    var xhr = $.ajax({
        type: "POST",
        async: true,
        url: APP_ROOT + "Ajax/GetFacilityMapData.aspx",
        dataType: "json",
        data: condition,
        traditional: true,
        success: function (data, status) {
            if (data != null) {
                try {
                    if (data["expired"] == true) {
                        window.top.location.href = ROOT_URL;
                    } else if (data["result"] == false) {
                        alert("施設データリストを取得できませんでした");
                    } else {
                        get_facility_map_data_completion(data, condition);
                    }
                }
                catch (e) {
                    alert("施設データリストを取得できませんでした");
                }
            }
            // Waitダイアログを閉じる
            CloseWaitDialog();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if (textStatus === 'abort') { return; }
            // Waitダイアログを閉じる
            CloseWaitDialog();
        }
    });
    jqXHR["get_facility_map_data"] = xhr;
};

// 施設データリストを取得
function get_facility_popup_data(facility_id, facility_kind) {
    // キャンセルリクエスト
    cancelRequest("get_facility_popup_data");
    var ret;

    var xhr = $.ajax({
        type: "POST",
        async: false,
        url: APP_ROOT + "Ajax/GetFacilityPopUpData.aspx",
        dataType: "json",
        data: { "ID": facility_id, "KIND": facility_kind },
        traditional: true,
        success: function (data, status) {
            if (data != null) {
                try {
                    if (data["expired"] == true) {
                        window.top.location.href = ROOT_URL;
                    } else if (data["result"] == false) {
                        alert("施設データリストを取得できませんでした");
                    } else {
                        //get_facility_popup_data_completion(data);
                        ret = data;
                    }
                }
                catch (e) {
                    alert("施設データリストを取得できませんでした");
                }
            }
            // Waitダイアログを閉じる
            CloseWaitDialog();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if (textStatus === 'abort') { return; }
        }
    });
    jqXHR["get_facility_popup_data"] = xhr;
    return ret;
};

// 施設データリストを取得
function get_facility_detail_data(facility_id, facility_kind) {
    // キャンセルリクエスト
    cancelRequest("get_facility_detail_data");
    var ret;

    var xhr = $.ajax({
        type: "POST",
        async: true,
        url: APP_ROOT + "Ajax/GetFacilityDetailData.aspx",
        dataType: "json",
        data: { "ID": facility_id, "KIND": facility_kind },
        traditional: true,
        success: function (data, status) {
            if (data != null) {
                try {
                    if (data["expired"] == true) {
                        window.top.location.href = ROOT_URL;
                    } else if (data["result"] == false) {
                        alert("施設データを取得できませんでした");
                    } else {
                        get_facility_detail_data_completion(facility_kind, data);
                        ret = data;
                    }
                }
                catch (e) {
                    alert("施設データを取得できませんでした");
                }
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if (textStatus === 'abort') { return; }
        }
    });
    jqXHR["get_facility_detail_data"] = xhr;
    return ret;
};

// 施設データリストを取得
function get_facility_data_list(strjson) {
    // キャンセルリクエスト
    cancelRequest("get_facility_data_list");

    var lefttop = "";
    var rightbottom = "";

    var xhr = $.ajax({
        type: "POST",
        async: true,
        url: APP_ROOT + "Ajax/GetFacilityDataList.aspx",
        data: strjson,
        dataType: "json",
        traditional: true,
        success: function (data, status) {
            if (data != null) {
                try {
                    if (data["expired"] == true) {
                        window.top.location.href = ROOT_URL;
                    } else if (data["result"] == false) {
                        alert("施設データリストを取得できませんでした");
                        // Waitダイアログを閉じる
                        CloseWaitDialog();
                    } else if (data["result"] == "empty") {
                        alert("条件に合致するデータがありません");
                        // Waitダイアログを閉じる
                        CloseWaitDialog();
                    } else {
                        get_facility_data_list_completion(data);
                    }
                }
                catch (e) {
                    alert("施設データリストを取得できませんでした");
                    // Waitダイアログを閉じる
                    CloseWaitDialog();
                }
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if (textStatus === 'abort') { return; }
            alert("施設データリストを取得できませんでした");
            // Waitダイアログを閉じる
            CloseWaitDialog();
        }
    });
    jqXHR["get_facility_data_list"] = xhr;
};

