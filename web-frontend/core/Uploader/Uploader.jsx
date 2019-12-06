import React, { Component } from 'react';
import { Upload, Modal } from 'antd';

const { Dragger } = Upload;

class Uploader extends Component {
    state = {
        previewVisible : false,
        previewImage : ''
    }

    getBase64 = file => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
        })
    }

    handlePreview = async file => {
        if (!file.url && !file.preview) {
            file.preview = await this.getBase64(file);
        }

        this.setState({
            previewImage : file.url || file.preview,
            previewVisible : true
        })
    }

    handleCancel = () => this.setState({ previewVisible : false })

    initProps = {
        multiple : true,
        listType : "picture-card",
        supportServerRender : true,
        customRequest : ({ file, onSuccess }) => {
            setTimeout(() => {
                onSuccess("ok");
            }, 0);
        },
        onPreview : this.handlePreview
    }

    render() {
        const fieldDecorator = this.props.fieldDecorator || (component => component);
        const { previewVisible, previewImage } = this.state;

        return (
            <div>
                {fieldDecorator(
                    <Dragger {...this.initProps} accept={this.props.accept}>
                        <p className="ant-upload-text">
                            ДОБАВИТЬ ФАЙЛЫ (не более 4-х штук, не более 5 МБ)
                        </p>
                    </Dragger>
                )}

                <Modal visible={previewVisible} footer={null} onCancel={this.handleCancel}>
                    <img src={previewImage} style={{width : '100%'}} />
                </Modal>
            </div>
        )
    }
}

export default Uploader;