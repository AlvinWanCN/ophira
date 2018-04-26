/**
 * Created by Alvin Wan on 4/24/2018.
 */


        function setCookie(name, value, iDay)
        {
            var oDate=new Date();
            oDate.setDate(oDate.getDate()+iDay);
            document.cookie=name+'='+encodeURIComponent(value)+';expires='+oDate;
        }
        function getCookie(name)
        {
            var arr=document.cookie.split('; ');
            var i=0;
            for(i=0;i<arr.length;i++)
            {
                //arr2->['username', 'abc']
                var arr2=arr[i].split('=');

                if(arr2[0]==name)
                {
                    var getC = decodeURIComponent(arr2[1]);
                    return getC;
                }
            }
            return '';
        }
        function removeCookie(name)
        {
            setCookie(name, '1', -1);
        }
    var app=new Vue({
        el: '#app',
        data: {
            visible: false,
            show_change_password:false,
            savePassLoading:false,
            cpassword:'',
            mpassword:'',
            fpassword:'',
            now:'',
            nickname:getCookie('nickname'),
            formPassword: {
                    oldpasswd: '',
                passwd: '',
                passwdCheck: '',
            },
            formLeft:{
                input1:'',
                input2:'',
                input3:'',
            },
        },
        delimiters:['${', '}'],

        methods: {
            show: function () {
                this.visible = true;
            },
            change_password:function () {
                this.show_change_password = true
            },
            confirm_password:function (name) {
                var lastUp = this;
                $.ajax({
                    type: "POST",//方法类型
                    dataType: "json",//预期服务器返回的数据类型
                    url: "/change_password" ,//url
                    data:name,
                    success: function (result) {
                        console.log(result);//打印服务端返回的数据(调试用)
                        if (result.code == 0) {
                            lastUp.show_change_password=false
                            lastUp.$Message.success(result.message)
                        }else {
                            lastUp.$Message.warning(result.message)
                        };
                    },
                    error : function() {
                        lastUp.$Message.error('something is error')
                    }
                });
            },
            cancel_update_password:function () {
             this.show_change_password=false
            },
            now_time:function () {
                 this.now = new Date().toTimeString();
            },
            to_index:function () {
                window.location.href="/";
            },
            load_account:function () {
                $('#index_content').load('/na',function (response,status,xhr) {
                })
            }
        }

    })

    setInterval('app.now_time()',1000);

