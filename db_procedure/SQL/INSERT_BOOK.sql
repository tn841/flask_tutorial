CREATE DEFINER=`root`@`localhost` PROCEDURE `INSERT_BOOK`(
	IN _BOOKID CHAR(5),
    IN _BOOKNAME VARCHAR(50), _PRICE DOUBLE, _BOOKTYPE VARCHAR(10),
    OUT RESULT INT	# -1:실패 0:성공
)
BEGIN
	/* 가격을 변경할 변수 선언 */
    DECLARE _SELLPRICE DOUBLE;

    /* SQL에러발생 시 ROLLBACK 처리*/
    DECLARE exit handler for SQLEXCEPTION
		BEGIN
			ROLLBACK;
		SET RESULT = -1;
	END;

    /* 트랜젝션 시작 */
    START TRANSACTION;
		/*BOOK insert*/
        INSERT INTO BOOKS(bookID, bookName, bookOriginPrice, bookType) VALUES (_BOOKID, _BOOKNAME, _PRICE, _BOOKTYPE);

        /*책 종류에 맞게 가격 조정*/
        IF _BOOKTYPE = 'novel' THEN
			SET _SELLPRICE = _PRICE + _PRICE * (10/100);
		ELSEIF _BOOKTYPE = 'art' THEN
			SET _SELLPRICE = _PRICE + _PRICE * (15/100);
		ELSE
			SET _SELLPRICE = _PRICE + _PRICE * (20/100);
		END IF;

        /*변경된 가격을 BOOKS_SELL에 저장*/
        INSERT INTO BOOKS_SELL(bookID, bookSellPrice, bookType) VALUES(_BOOKID, _SELLPRICE, _BOOKTYPE);

    /* commit */
    COMMIT;
    SET RESULT = 0;
END