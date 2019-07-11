import { Button, Col, Drawer, Icon, Row } from 'antd';
import * as React from 'react';
import MediaQuery from 'react-responsive';
import { NavLink, Route, Switch, Link } from 'react-router-dom';
import './App.scss';
import Home from './components/Home';
import CountyCandidates from './components/CountyCandidates/CountyCandidates';
import ConstituencyPage from './components/ConstituencyDistrict/Constituency';
import County from './components/CountyConstituency/County';
import './static/style/button.scss';
import LegislatorList from './components/Legislator/LegislatorList';

interface State {
    visible: boolean;
}

class App extends React.Component<{}, State> {
    state = { visible: false };
    showDrawer = (): void => {
        this.setState({
            visible: true
        });
    };

    onClose = (): void => {
        this.setState({
            visible: false
        });
    };

    render() {
        return (
            <Row
                className="main-page"
                style={{ minHeight: window.innerHeight }}
            >
                <Row className="header">
                    <Col span={1}>
                        <Button type="ghost" onClick={this.showDrawer}>
                            <Icon type="menu" style={{ color: 'white' }} />
                        </Button>
                    </Col>
                    <Col span={22}>
                        <Row>
                            <MediaQuery minDeviceWidth={300}>
                                <Row className="nav">
                                    <ul>
                                        <NavLink exact to="/">
                                            <li className="appName">
                                                2020 投票指南
                                            </li>
                                        </NavLink>
                                    </ul>
                                </Row>
                            </MediaQuery>
                        </Row>
                    </Col>
                    <Col span={1} />
                </Row>
                <Row className="contentBox">
                    <Row className="content">
                        <Switch>
                            <Route exact path="/" component={Home} />
                            <Route exact path="/regionals" component={County} />
                            <Route
                                exact
                                path="/regionals/:county"
                                component={ConstituencyPage}
                            />
                            <Route
                                exact
                                path="/regionals/:county/:district"
                                component={CountyCandidates}
                            />
                        </Switch>
                    </Row>
                </Row>
                <Drawer
                    title="選區找立委"
                    placement="left"
                    closable={false}
                    onClose={this.onClose}
                    visible={this.state.visible}
                >
                    <p>
                        <Link to="/regionals">比較區域立委</Link>
                    </p>
                    <p>Some contents...</p>
                    <p>Some contents...</p>
                </Drawer>
            </Row>
        );
    }
}

export default App;
