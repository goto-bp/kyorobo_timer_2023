class Team
{
    name;
    point;
    nameElem;
    pointElem;
    offsetPoint = 5;
};

var red = new Team();
var blue = new Team();

red.name = "赤チーム";
red.point = 0;
red.nameElem = document.getElementById("red-name");
red.pointElem = document.getElementById("red-point");
blue.name = "青チーム";
blue.point = 0;
blue.nameElem = document.getElementById("blue-name");
blue.pointElem = document.getElementById("blue-point");


function countdown()
{
    elem = document.getElementById("countdown");
    var count = 5;
    elem.innerHTML = count;
    var id = setInterval(function()
    {
        count--;
        console.log(count);
        elem.innerHTML = count;
        if(count == 0)
        {
            elem.innerHTML = "Start!!";
            elem.style.fontSize = "20em";
        }
        else if(count < 0)
        {
            elem.style.display = "none";
            elem.style.fontSize = "32em";
            startTimer();
            clearInterval(id);
        }
    }, 1000);

}

class Timer
{
    time;
    timeElem;
    set_time(min, sec)
    {
        this.time = min * 60 + sec;
    }
    time_to_str()
    {
        var min = Math.floor(this.time / 60);
        var sec = this.time % 60;
        var sec = ( '00' + sec ).slice( -2 );
        return min + ":" + sec;
    }
}

var timer = new Timer();
timer.set_time(2, 30);
timer.timeElem = document.getElementById("timer");
timer.timeElem.innerHTML = timer.time_to_str();


function addPoint(team, point = 1)
{
    team.point += point;
    team.pointElem.innerHTML = team.point;
}

function subPoint(team, point = 1)
{
    team.point -= point;
    if(team.point < 0)
        team.point = 0;
    team.pointElem.innerHTML = team.point;
}

function resetPoint(team)
{
    team.point = 0;
    team.pointElem.innerHTML = team.point;
}

function startTimer()
{
    red.nameElem.innerHTML = red.name;
    blue.nameElem.innerHTML = blue.name;
    red.pointElem.innerHTML = red.point;
    blue.pointElem.innerHTML = blue.point;

    // タイマー
    id = setInterval(function()
    {
        console.log(timer.time);
        if (timer.time > 0)
            timer.time--;
        if(timer.time <= 0)
        {
            timer.timeElem.style.color = "red";
            clearInterval(id);
        }
        timer.timeElem.innerHTML = timer.time_to_str();

    }, 1000);

    function timerKey(e)
    {
        // 1
        if(e.keyCode == 49)
        {
            resetPoint(red);
        }
        // w
        else if(e.keyCode == 87)
        {
            addPoint(red);
        }
        // s
        else if(e.keyCode == 83)
        {
            subPoint(red);
        }
        //d
        else if(e.keyCode == 68)
        {
            addPoint(red, red.offsetPoint);
        }
        // a
        else if(e.keyCode == 65)
        {
            subPoint(red, red.offsetPoint);
        }
        // 2
        else if(e.keyCode == 50)
        {
            resetPoint(blue);
        }
        // upkey
        else if(e.keyCode == 38)
        {
            addPoint(blue);
        }
        // downkey
        else if(e.keyCode == 40)
        {
            subPoint(blue);
        }
        // rightkey
        else if(e.keyCode == 39)
        {
            addPoint(blue, blue.offsetPoint);
        }
        // leftkey
        else if(e.keyCode == 37)
        {
            subPoint(blue, blue.offsetPoint);
        }
        //esc
        else if(e.keyCode == 27)
        {
            clearInterval(id);
            elem = document.getElementById("title");
            elem.style.display = "block";
            elem = document.getElementById("countdown");
            elem.style.display = "block";
            elem.innerHTML = "5";
            timer.set_time(2, 30);
            timer.timeElem.innerHTML = timer.time_to_str();
            timer.timeElem.style.color = "white";
            red.point = 0;
            blue.point = 0;
            document.removeEventListener("keydown", timerKey);
            clearInterval(id);

            startscreen();
        }
    }

    // keydownイベント
    document.addEventListener("keydown", timerKey);


}


function startscreen()
{
    var elem = document.getElementById("title");
    var setting_elem = document.getElementById("setting-screen");
    var setting_elem_list = [
        document.getElementById("change-team-name"),
        document.getElementById("set-time"),
        document.getElementById("set-point")
    ]
    var cursor = [0, 0];

    function startKey(e)
    {
        // shift
        if(e.keyCode == 16)
        {
            if(setting_elem.style.display == "block")
            {
                setting_elem.style.display = "none";
            }
            else
            {
                setting_elem.style.display = "block";
                setting_elem_list[cursor[0]].style.color = "red";
            }
        }
        // up
        else if(e.keyCode == 38)
        {
            if(setting_elem.style.display == "block")
            {
                setting_elem_list[cursor[0]].style.color = "white";
                cursor[0]--;
                if(cursor[0] < 0)
                    cursor[0] = setting_elem_list.length - 1;
                setting_elem_list[cursor[0]].style.color = "red";
            }
        }
        // down
        else if(e.keyCode == 40)
        {
            if(setting_elem.style.display == "block")
            {
                setting_elem_list[cursor[0]].style.color = "white";
                cursor[0]++;
                if(cursor[0] >= setting_elem_list.length)
                    cursor[0] = 0;
                setting_elem_list[cursor[0]].style.color = "red";
            }
        }
        //enter
        if(e.keyCode == 13)
        {
            if(setting_elem.style.display == "block")
            {
                if(cursor[0] == 0)
                {
                    
                }
            }
            else
            {
                elem.style.display = "none";
                document.removeEventListener("keydown", startKey);
                countdown();
            }
        }
    }
    document.addEventListener("keydown", startKey);

}

window.onload = function()
{
    startscreen();
}