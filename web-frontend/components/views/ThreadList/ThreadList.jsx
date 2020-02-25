import React, { Component } from 'react';

import Thread from '../Thread/Thread.jsx';

class ThreadList extends Component {
    static COLUMN = 'column';
    static FLEX = 'flex';

    columnList = () => {
        const data = this.props.data;
        
        return (
            <div>
                {data.map((el, id) => (
                    <Thread
                        key={id}
                        mode={Thread.COLUMN}
                        data={el}
                    />
                ))}
            </div>
        )
    }
    
    render() {
        const mode = this.props.mode || ThreadList.COLUMN;

        if (mode === ThreadList.COLUMN) {
            return this.columnList();
        } else {
            return null;
        }
    }
}

export default ThreadList;