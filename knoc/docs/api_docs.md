# Knoc API Docs
***

## POST API
> POST APIs for Knoc, including create/get items apis, get groups apis.

### 获取小组列表
* URL  `/api/post/group/`
* Method `GET`
* Params `None`
* Response

```
{
    "msg": "SUCCESS",
    "status_code": 0,
    "data": [
        {
            "id": 2,
            "name": "shanbay"
        },
        {
            "id": 3,
            "name": "py"
        },
        {
            "id": 4,
            "name": "Android"
        },
        {
            "id": 5,
            "name": "iOS"
        }
    ]
} 
```

### 获取本组的Item数据
* URL `/api/post/link/<group_id>/`
* Method `GET`
* Params `None`
* Response

```
{
    "msg": "SUCCESS",
    "status_code": 0,
    "data": {
        "items": [
            {
                "update_time": "2015-04-25T13:43:14.545Z",
                "author_info": {
                    "username": "jinchang",
                    "id": 1
                },
                "title": "扇贝网，英语听说读写和词汇，我们都能帮到你 扇贝英语",
                "object_id": 2,
                "item_type": "link",
                "create_time": "2015-04-22T09:08:01.353Z",
                "group_id": 4,
                "id": 3,
                "tag_str": "教育,英语"
            }
        ],
        "ipp": 10,
        "total": 1
    }
}
```

### 生成URL记录
* URL `/api/post/link/<group_id>/`
* Method `POST`
* Params

```
{
	link: '<URL>'
}
```
* Response

	


```
{
    "msg": "SUCCESS",
    "status_code": 0,
    "data": {
        "update_time": "2015-04-26T06:57:30.581Z",
        "author_info": {
            "username": "jinchang",
            "id": 1
        },
        "title": "扇贝网，英语听说读写和词汇，我们都能帮到你 扇贝英语",
        "object_id": 4,
        "item_type": "link",
        "create_time": "2015-04-26T06:57:30.581Z",
        "group_id": "1",
        "id": 5,
        "tag_str": ""
    }
}
```