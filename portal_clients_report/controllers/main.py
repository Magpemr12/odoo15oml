# -*- coding: utf-8 -*-
import base64
import zipfile
import io
import logging
import json
from odoo import http
from odoo.http import request, content_disposition
logger = logging.getLogger(__name__)


class ZipMaker(http.Controller):

    def _make_zip(self, name, attachments):
        stream = io.BytesIO()
        try:
            with zipfile.ZipFile(stream, 'w') as doc_zip:
                for attachment in attachments:
                    if attachment.type in ['url', 'empty']:
                        continue
                    filename = attachment.datas_fname
                    doc_zip.writestr(filename, base64.b64decode(attachment['datas']), compress_type=zipfile.ZIP_DEFLATED)
        except zipfile.BadZipfile:
            logger.exception("BadZipfile exception")

        content = stream.getvalue()
        headers = [
            ('Content-Type', 'zip'),
            ('X-Content-Type-Options', 'nosniff'),
            ('Content-Length', len(content)),
            ('Content-Disposition', content_disposition(name))
        ]
        return request.make_response(content, headers)

    @http.route(['/download/zip/<string:zip_name>/<string:ids>'], type='http', auth='public')
    def _get_zip(self, zip_name, ids, **kwargs):
        try:
            zip_name = 'payment.zip'
            # e.g. http://localhost:8069/download/zip/test.zip/[462,364]
            ids = json.loads(ids)
            attachments = request.env['ir.attachment'].sudo().browse(ids)
            return self._make_zip(zip_name, attachments)
        except Exception as ex:
            return request.not_found()
