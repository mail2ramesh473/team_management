# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from copy import deepcopy

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from teams.forms import TeamForm
from teams.models import Team


def validate_request(req_data):
    for re_key in req_data:
        if re_key in ['firstName', 'lastName', 'phone', 'emailId', 'role']:
            return True
    return False


def format_response(response):
    new_response = deepcopy(response)
    for res_key in new_response:
        if res_key not in ['userId', 'firstName', 'lastName', 'phone', 'emailId', 'role']:
            response.pop(res_key)
    return response


def getMemberInstance(mem_id):
    try:
        instance = Team.objects.get(pk=mem_id)
    except Team.DoesNotExist:
        instance = None

    return instance


@csrf_exempt
def add_team_member(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        valid_req = validate_request(post_data)
        if valid_req:
            role = post_data.get('role')
            role_val = 'admin' if role in (1, 'admin') else 'regular'
            post_data['role'] = role_val
            unq_id = post_data.get('userId')
            if not unq_id:
                team_obj = TeamForm(post_data)
                if team_obj.is_valid():
                    final_model = team_obj.save()
                    unique_id = final_model.pk
                    post_data['userId'] = unique_id
                    response = format_response(post_data)
                    http_response = HttpResponse(json.dumps(response), content_type="application/json")
                    return http_response
        else:
            return HttpResponseBadRequest(content="Neither of required fields are present in Request payload")

    return HttpResponseBadRequest(content="Tested Suucessfully")


@csrf_exempt
def update_team_member(request):
    if request.method in ["PUT", "POST"]:
        post_data = json.loads(request.body)
        role = post_data.get('role')
        if role:
            role_val = 'admin' if role in (1, 'admin') else 'regular'
            post_data['role'] = role_val
        unq_id = post_data.get('userId')
        if unq_id:
            valid_req = validate_request(post_data)
            if valid_req:
                instance = getMemberInstance(unq_id)
                if instance:
                    for ke, kv in post_data.iteritems():
                        instance.__setattr__(ke, kv)
                        instance.save()
                    return_resp = {"success": True, "message": "Document Updated Successfully"}
                    http_response = HttpResponse(json.dumps(return_resp), content_type="application/json")
                else:
                    http_response = HttpResponseBadRequest(content="Document not exists")
            else:
                resp_data = "Required fields are not present to update or nothing to update"
                http_response = HttpResponseBadRequest(content=resp_data)
        else:
            http_response = HttpResponseBadRequest(content="Missing userId to update Team Member")
    else:
        http_response = HttpResponseBadRequest(content="Required PUT/POST Method to update data")

    return http_response


@csrf_exempt
def delete_team_memeber(request):
    req_method = request.method
    if req_method in ['DELETE']:
        post_data = json.loads(request.body)
        user_id = post_data.get('userId', '')
        if user_id:
            instance = getMemberInstance(user_id)
            if instance:
                instance.delete()
                return_resp = {"success": True, "message": "Deleted Document Successfully"}
                http_response = HttpResponse(json.dumps(return_resp), content_type="application/json")
            else:
                http_response = HttpResponseBadRequest(content="Document not exists")
        else:
            http_response = HttpResponseBadRequest(content="Missing userId to delete team member")
    else:
        http_response = HttpResponseBadRequest(content="Required DELETE Method to delete team member")

    return http_response
