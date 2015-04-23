<%inherit file="_master.mako"></%inherit>

<%block name="title">Логин</%block>

<%block name="css">
    <link href="${request.static_url('metro4all:static/contrib/jtable.2.4.0/themes/metro/metro4all/jtable.css')}"
          rel="stylesheet" type="text/css"/>
    <link href="${request.static_url('metro4all:static/css/reports.css')}"
          rel="stylesheet" type="text/css"/>
</%block>

<div class="row">
    <div class="col s12">
        <p>Для редактирования у вас недостаточно прав.<br/>
            Если вы не администратор - вернитесь к просмотру таблицы по этой <a href="${request.route_url('home')}">ссылке</a>.<br/>
            Если у вас есть права администратора - введите свой логин и пароль в форму ниже.
        </p>
    </div>
</div>
<div class="row">
    <div class="row">
        <form class="col s12">
            <input type="hidden" name="came_from" value="${came_from}"/>
            %if message:
                <div class="row">
                    <div class="col s12">
                        <div class="card red darken-1">
                            <div class="card-content white-text">
                                <p>${message}</p>
                            </div>
                        </div>
                    </div>
                </div>
            %endif
            <div class="row">
                <div class="input-field col s6">
                    <input placeholder="Логин" id="login" name="login" type="text" class="validate" value="${login}">
                    <label for="first_name">Логин</label>
                </div>
            </div>
            <div class="row">
                <div class="input-field col s6">
                    <input id="password" name="password" type="password" class="validate" value="${password}"/>
                    <label for="password">Password</label>
                </div>
            </div>

            <div class="row">
                <div class="input-field col s6">
                    <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                        <i class="mdi-content-send right"></i>
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>