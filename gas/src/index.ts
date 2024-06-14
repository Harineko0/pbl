// GASから参照したい変数はglobalオブジェクトに渡してあげる必要がある
(global as any).sample = () => {
    console.log("hello world");
};
