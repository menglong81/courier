from django.shortcuts import render, redirect, HttpResponse
from app_website import models as website_models

import json
import traceback
from common.log import MAIN_LOG

def quick_record(request):
    try:
        if request.method == 'GET':
            context = {
                'title': '快速录入',
            }
            return render(request, 'hui/quick_record.html', context)
        else:
            word_english = request.POST.get('word_english')
            word_chinese = request.POST.get('word_chinese')
            # if None in [word_chinese, word_english]:
            #     return HttpResponse(json.dumps({'status': 'alert', 'msg': '填写完整'}))

            website_models.Word.objects.create(word_chinese=word_chinese, word_english=word_english)
            return HttpResponse(json.dumps({'status': 'ok', 'msg': 'ok'}))
    except Exception as e:
        MAIN_LOG.logger.error(traceback.format_exc())
        return HttpResponse(json.dumps({'status': 'error', 'msg': str(e)}))


