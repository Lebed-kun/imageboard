import React from 'react';
import { Modal, Form, Input, Button } from 'antd';



/**
 * 
 * @param {object} param0
 * @property {boolean} openReportModal
 * @returns {React.ReactElement} 
 */
const ReportForm = ({ openReportModal, reportPosts }) => (
    <Modal visible={openReportModal}>
        <Form onFinish={async values => await reportPosts(values.reason)}>
            <Form.Item name="reason">
                <Input.TextArea name="reason" placeholder="Причина жалобы" />
            </Form.Item>

            <Button type="primary" htmlType="submit">
                Отправить
            </Button>
        </Form>
    </Modal>
)

export default ReportForm;